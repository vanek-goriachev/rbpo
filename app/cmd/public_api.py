import os

from fastapi import FastAPI

from app.domain.services.post import PostService
from app.domain.services.post_tag import PostTagService
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.post import PostRepository
from app.storage.postgres.post_tag import PostTagRepository
from app.transport.rest.fast_api.public import PublicAPI

# Получаем параметры подключения к БД из переменных окружения
db_host = os.getenv("DB_HOST", "postgres")
db_port = int(os.getenv("DB_PORT", "5432"))
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if not all([db_name, db_user, db_password]):
    raise ValueError(
        "Необходимые переменные окружения для БД не установлены: DB_NAME, DB_USER, DB_PASSWORD"
    )

# Создаем и инициализируем менеджер БД
db_manager = DatabaseManager()
db_manager.initialize(db_host, db_port, db_name, db_user, db_password)
db_manager.create_tables()

# PostgreSQL репозитории с инъекцией зависимостей
post_repository = PostRepository(db_manager)
post_tags_repository = PostTagRepository(db_manager)

# domain
post_service = PostService(post_repository, post_tags_repository)
post_tags_service = PostTagService(post_tags_repository)

# transport
fastapi_app = FastAPI(title="SimpleBlog public API", version="0.1.0")

public_api = PublicAPI(fastapi_app, post_service, post_tags_service)
public_api.register()
