"""
Пример использования транзакций в бизнес-логике
"""

import uuid
from datetime import datetime

from sqlalchemy.engine import IsolationLevel

from app.domain.models.post import Post
from app.domain.models.user import User
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.post import PostRepository
from app.storage.postgres.post_tag import PostTagRepository
from app.storage.postgres.user import UserRepository


class TransactionExample:
    """Пример использования транзакций в бизнес-логике"""

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager
        self._user_repo = UserRepository(db_manager)
        self._post_repo = PostRepository(db_manager)
        self._post_tag_repo = PostTagRepository(db_manager)

    def create_user_with_first_post(
        self, username: str, post_title: str, post_body: str, tags: list[str]
    ):
        """
        Пример бизнес-операции: создать пользователя и его первый пост в одной транзакции
        """
        with self._db_manager.transaction() as session:
            # Создаем пользователя
            user = User(id_=uuid.uuid4(), username=username)
            self._user_repo.create_user(user, session)

            # Создаем теги для поста
            post_tags = []
            for tag_name in tags:
                tag = self._post_tag_repo.get_or_create_post_tag(tag_name, session)
                post_tags.append(tag)

            # Создаем пост
            now = datetime.utcnow()
            post = Post(
                id_=uuid.uuid4(),
                title=post_title,
                body=post_body,
                status="draft",
                created_at=now,
                updated_at=now,
                tags=post_tags,
            )
            self._post_repo.create_post(post, session)

            # Если все прошло успешно, транзакция автоматически коммитится
            return user, post

    def transfer_post_between_users(self, post_id: uuid.UUID, from_username: str, to_username: str):
        """
        Пример бизнес-операции: передать пост от одного пользователя другому
        Использует уровень изоляции READ_COMMITTED
        """
        with self._db_manager.transaction(IsolationLevel.READ_COMMITTED) as session:
            # Получаем пост
            post = self._post_repo.get_post_by_id(post_id, session)

            # Проверяем, что пост принадлежит исходному пользователю
            from_user = self._user_repo.get_user_by_username(from_username, session)
            if not from_user:
                raise ValueError(f"Пользователь {from_user} не найден")

            # Проверяем, что целевой пользователь существует
            to_user = self._user_repo.get_user_by_username(to_username, session)
            if not to_user:
                raise ValueError(f"Пользователь {to_username} не найден")

            # Обновляем пост (в реальности здесь была бы логика передачи прав)
            post.updated_at = datetime.utcnow()
            self._post_repo.update_post(post, session)

            return post

    def bulk_create_posts_with_tags(self, posts_data: list[dict]):
        """
        Пример массовой операции: создать несколько постов с тегами в одной транзакции
        Использует уровень изоляции SERIALIZABLE для предотвращения конфликтов
        """
        with self._db_manager.transaction(IsolationLevel.SERIALIZABLE) as session:
            created_posts = []

            for post_data in posts_data:
                # Создаем теги
                post_tags = []
                for tag_name in post_data.get("tags", []):
                    tag = self._post_tag_repo.get_or_create_post_tag(tag_name, session)
                    post_tags.append(tag)

                # Создаем пост
                now = datetime.utcnow()
                post = Post(
                    id_=uuid.uuid4(),
                    title=post_data["title"],
                    body=post_data["body"],
                    status=post_data.get("status", "draft"),
                    created_at=now,
                    updated_at=now,
                    tags=post_tags,
                )
                self._post_repo.create_post(post, session)
                created_posts.append(post)

            return created_posts

    def complex_business_operation(
        self, user_id: uuid.UUID, post_id: uuid.UUID, new_tags: list[str]
    ):
        """
        Пример сложной бизнес-операции: обновить пользователя, пост и добавить теги
        Использует уровень изоляции REPEATABLE_READ
        """
        with self._db_manager.transaction(IsolationLevel.REPEATABLE_READ) as session:
            # Получаем пользователя
            user = self._user_repo.get_user_by_id(user_id, session)

            # Получаем пост
            post = self._post_repo.get_post_by_id(post_id, session)

            # Обновляем пользователя
            user.username = f"{user.username}_updated"
            self._user_repo.update_user(user, session)

            # Создаем новые теги
            new_tag_objects = []
            for tag_name in new_tags:
                tag = self._post_tag_repo.get_or_create_post_tag(tag_name, session)
                new_tag_objects.append(tag)

            # Добавляем теги к посту
            self._post_repo.add_tags(post_id, new_tag_objects, session)

            # Обновляем пост
            post.updated_at = datetime.utcnow()
            self._post_repo.update_post(post, session)

            return user, post
