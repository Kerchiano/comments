# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/

# Собираем статику
RUN python manage.py collectstatic --noinput

# Открываем порт для приложения
EXPOSE 8000

# Запускаем приложение
CMD ["daphne", "-p", "8000", "comments.asgi:application"]