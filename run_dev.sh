#!/bin/bash

echo "Запуск SimpleBlog в режиме разработки..."

# Создаем .env файл если его нет
if [ ! -f .env ]; then
    echo "Создаем .env файл из примера..."
    cp env.example .env
    echo "Файл .env создан. Вы можете отредактировать его при необходимости."
fi

# Запускаем приложение
echo "Запускаем Docker Compose..."
docker-compose --profile=dev --env-file=.env up --build

echo "Приложение запущено!"
echo "API доступно по адресу: http://localhost:8000"
