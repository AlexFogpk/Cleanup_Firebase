# Используем базовый образ с Python 3.9 (slim версия)
FROM python:3.9-slim

# Устанавливаем cron (и необходимые утилиты)
RUN apt-get update && apt-get install -y cron

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем cron-таблицу в нужное место
COPY cleanup-cron /etc/cron.d/cleanup-cron
# Делаем файл доступным для чтения
RUN chmod 0644 /etc/cron.d/cleanup-cron
# Регистрируем cron-таблицу
RUN crontab /etc/cron.d/cleanup-cron

# Запускаем cron в форграунде, чтобы контейнер не завершился
CMD ["cron", "-f"]
