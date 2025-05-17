import argparse
import requests
import psycopg2
import ipaddress
from collections import defaultdict
from dotenv import load_dotenv
import sys
import os

# Загрузка переменных окружения из .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def load_ips_from_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Ошибка: файл '{file_path}' не найден.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def group_ips_by_subnet(ip_list, subnet_mask):
    subnets = defaultdict(list)
    for ip in ip_list:
        try:
            network = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)
            subnet_str = f"{network.network_address}/{subnet_mask}"
            subnets[subnet_str].append(ip)
        except ValueError:
            print(f"Пропущен некорректный IP: {ip}")
    return subnets

def main():
    parser = argparse.ArgumentParser(description="Обработка IP-адресов по подсетям")
    parser.add_argument("file", help="Путь до файла со списком IP-адресов")
    parser.add_argument("--mask", type=int, default=24, help="Маска подсети (по умолчанию 24)")
    args = parser.parse_args()

    ip_list = load_ips_from_file(args.file)
    subnets = group_ips_by_subnet(ip_list, args.mask)

    # Подключение к бд
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Создание таблицы, если не существует
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ip_info (
        id SERIAL PRIMARY KEY,
        subnet TEXT UNIQUE,
        provider TEXT,
        country TEXT
    )
    """)
    conn.commit()

    processed_subnets = set()

    for subnet, ips in subnets.items():
        if subnet in processed_subnets:
            continue

        sample_ip = ips[0]
        response = requests.get(f"http://ip-api.com/json/{sample_ip}?fields=isp,country,status,message")
        data = response.json()

        if data["status"] == "success":
            provider = data["isp"]
            country = data["country"]
            print(f"{subnet} → {provider} ({country})")

            cursor.execute("""
                INSERT INTO ip_info (subnet, provider, country)
                VALUES (%s, %s, %s)
                ON CONFLICT (subnet) DO UPDATE
                SET provider = EXCLUDED.provider,
                    country = EXCLUDED.country
            """, (subnet, provider, country))

            processed_subnets.add(subnet)
        else:
            print(f"Ошибка для IP {sample_ip}: {data.get('message')}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
