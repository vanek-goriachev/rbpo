-- Инициализация базы данных для SimpleBlog
-- Этот файл выполняется при первом запуске PostgreSQL контейнера

-- Создание расширений если необходимо
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- База данных и пользователь уже созданы через переменные окружения
-- Здесь можно добавить дополнительные настройки или данные по умолчанию

-- Создание индексов для оптимизации производительности
-- (SQLAlchemy создаст таблицы автоматически, но индексы можно добавить здесь)

-- Пример создания индексов (будут созданы после создания таблиц SQLAlchemy):
-- CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
-- CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
-- CREATE INDEX IF NOT EXISTS idx_post_tags_name ON post_tags(name);
-- CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
