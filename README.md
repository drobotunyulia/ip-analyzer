# IP Subnet Analyzer  

Скрипт для группировки IP-адресов по подсетям, определения провайдера и страны через API, сохранения данных в PostgreSQL.  

## Функционал  
- Группировка IP-адресов по подсетям с настраиваемой маской (по умолчанию `/24`).  
- Запрос к [ip-api.com](https://ip-api.com) для получения провайдера и страны.  
- Сохранение результатов в PostgreSQL с обработкой дубликатов.  
- Конфигурация через `.env` и аргументы командной строки.  

## Технологии  
- Python 3.8+  
- Библиотеки:  
  - `requests` — HTTP-запросы к API.  
  - `ipaddress` — работа с IP-адресами.  
  - `psycopg2-binary` — взаимодействие с PostgreSQL.  
  - `python-dotenv` — загрузка переменных окружения.  
- СУБД: PostgreSQL  

## Установка  
1. Клонируйте репозиторий:  
   ```bash  
   git clone https://github.com/yourusername/ip-subnet-analyzer.git  
   cd ip-subnet-analyzer
Установите зависимости:


pip install -r requirements.txt  
Создайте файл .env в корне проекта:

DB_NAME=your_db_name  
DB_USER=your_username  
DB_PASSWORD=your_password  
DB_HOST=localhost  
DB_PORT=5432  


Подготовьте файл с IP-адресами (например, ips.txt):


## Запуск

Запуск с маской /24:

python ip_subnets.py /path/to/ips.txt --mask 24

Запуск с маской /16:

python ip_subnets.py ips.txt --mask 16  

Обновление существующих записей: при повторном запуске данные обновляются.
