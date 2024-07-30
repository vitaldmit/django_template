# Используем официальный образ Python 3.12
FROM python:3.12

# Устанавливаем переменную окружения для работы Python в неинтерактивном режиме
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Запускаем Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
