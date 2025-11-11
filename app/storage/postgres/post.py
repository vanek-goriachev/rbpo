import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.interfaces.storage.post import PostRepository as PostRepositoryInterface
from app.domain.models.errors.domain import NotFoundError
from app.domain.models.post import Post
from app.domain.models.post_tag import PostTag
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.models import PostModel, PostTagModel


class PostRepository(PostRepositoryInterface):
    """PostgreSQL репозиторий для постов"""

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def create_post(self, post: Post, session: Optional[Session] = None) -> None:
        """Создать новый пост"""
        if session is not None:
            return self._create_post_with_session(session, post)

        with self._db_manager.get_session() as session:
            return self._create_post_with_session(session, post)

    def _create_post_with_session(self, session: Session, post: Post) -> None:
        """Внутренний метод для создания поста"""

        post_model = PostModel(
            id=post.id_,
            title=post.title,
            body=post.body,
            status=post.status,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

        session.add(post_model)
        if not session.in_transaction():
            session.commit()

    def get_post_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> Post:
        """Получить пост по ID"""
        if session is not None:
            return self._get_post_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._get_post_by_id_with_session(session, id_)

    def _get_post_by_id_with_session(self, session: Session, id_: uuid.UUID) -> Post:
        """Внутренний метод для получения поста по ID"""
        post_model = session.query(PostModel).filter(PostModel.id == id_).first()

        if not post_model:
            raise NotFoundError(instance_type=Post)

        # Преобразуем теги из модели в доменные объекты
        tags = []
        if post_model.tags:
            tags = [PostTag(id_=tag.id, name=tag.name) for tag in post_model.tags]

        return Post(
            id_=post_model.id,
            title=post_model.title,
            body=post_model.body,
            status=post_model.status,
            created_at=post_model.created_at,
            updated_at=post_model.updated_at,
            tags=tags,
        )

    def update_post(self, post: Post, session: Optional[Session] = None) -> None:
        """Обновить пост"""
        if session is not None:
            return self._update_post_with_session(session, post)

        with self._db_manager.get_session() as session:
            return self._update_post_with_session(session, post)

    def _update_post_with_session(self, session: Session, post: Post) -> None:
        """Внутренний метод для обновления поста"""
        post_model = session.query(PostModel).filter(PostModel.id == post.id_).first()

        if not post_model:
            raise NotFoundError(instance_type=Post)

        # Обновляем основные поля
        post_model.title = post.title
        post_model.body = post.body
        post_model.status = post.status
        post_model.updated_at = post.updated_at

        # Обновляем теги
        if post.tags:
            tag_ids = [tag.id_ for tag in post.tags]
            tag_models = session.query(PostTagModel).filter(PostTagModel.id.in_(tag_ids)).all()
            post_model.tags = tag_models
        else:
            post_model.tags = []

        if not session.in_transaction():
            session.commit()

    def list_posts_by_filters(self, *args, **kwargs) -> List[Post]:
        """Получить список постов с фильтрацией"""
        with self._db_manager.get_session() as session:
            query = session.query(PostModel)

            # Применяем фильтры
            if "status" in kwargs:
                query = query.filter(PostModel.status == kwargs["status"])

            if "title_contains" in kwargs:
                query = query.filter(PostModel.title.contains(kwargs["title_contains"]))

            if "created_after" in kwargs:
                query = query.filter(PostModel.created_at >= kwargs["created_after"])

            if "created_before" in kwargs:
                query = query.filter(PostModel.created_at <= kwargs["created_before"])

            # Сортировка
            order_by = kwargs.get("order_by", "created_at")
            order_direction = kwargs.get("order_direction", "desc")

            if order_direction == "desc":
                query = query.order_by(getattr(PostModel, order_by).desc())
            else:
                query = query.order_by(getattr(PostModel, order_by).asc())

            # Пагинация
            limit = kwargs.get("limit")
            offset = kwargs.get("offset", 0)

            if limit:
                query = query.limit(limit).offset(offset)

            post_models = query.all()

            # Преобразуем в доменные объекты
            posts = []
            for post_model in post_models:
                tags = []
                if post_model.tags:
                    tags = [PostTag(id_=tag.id, name=tag.name) for tag in post_model.tags]

                posts.append(
                    Post(
                        id_=post_model.id,
                        title=post_model.title,
                        body=post_model.body,
                        status=post_model.status,
                        created_at=post_model.created_at,
                        updated_at=post_model.updated_at,
                        tags=tags,
                    )
                )

            return posts

    def delete_post_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> None:
        """Удалить пост по ID"""
        if session is not None:
            return self._delete_post_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._delete_post_by_id_with_session(session, id_)

    def _delete_post_by_id_with_session(self, session: Session, id_: uuid.UUID) -> None:
        """Внутренний метод для удаления поста"""
        post_model = session.query(PostModel).filter(PostModel.id == id_).first()

        if not post_model:
            raise NotFoundError(instance_type=Post)

        session.delete(post_model)
        if not session.in_transaction():
            session.commit()

    def add_tags(
        self, id_: uuid.UUID, tags: List[PostTag], session: Optional[Session] = None
    ) -> None:
        """Добавить теги к посту"""
        if session is not None:
            return self._add_tags_with_session(session, id_, tags)

        with self._db_manager.get_session() as session:
            return self._add_tags_with_session(session, id_, tags)

    def _add_tags_with_session(self, session: Session, id_: uuid.UUID, tags: List[PostTag]) -> None:
        """Внутренний метод для добавления тегов к посту"""
        post_model = session.query(PostModel).filter(PostModel.id == id_).first()

        if not post_model:
            raise NotFoundError(instance_type=Post)

        # Получаем существующие теги
        existing_tag_ids = {tag.id for tag in post_model.tags}

        # Получаем новые теги из базы данных
        new_tag_ids = [tag.id_ for tag in tags if tag.id_ not in existing_tag_ids]
        if new_tag_ids:
            new_tag_models = (
                session.query(PostTagModel).filter(PostTagModel.id.in_(new_tag_ids)).all()
            )
            post_model.tags.extend(new_tag_models)
            if not session.in_transaction():
                session.commit()

    def remove_tags(
        self, id_: uuid.UUID, tags: List[PostTag], session: Optional[Session] = None
    ) -> None:
        """Удалить теги из поста"""
        if session is not None:
            return self._remove_tags_with_session(session, id_, tags)

        with self._db_manager.get_session() as session:
            return self._remove_tags_with_session(session, id_, tags)

    def _remove_tags_with_session(
        self, session: Session, id_: uuid.UUID, tags: List[PostTag]
    ) -> None:
        """Внутренний метод для удаления тегов из поста"""
        post_model = session.query(PostModel).filter(PostModel.id == id_).first()

        if not post_model:
            raise NotFoundError(instance_type=Post)

        # Получаем ID тегов для удаления
        tag_ids_to_remove = {tag.id_ for tag in tags}

        # Удаляем теги
        post_model.tags = [tag for tag in post_model.tags if tag.id not in tag_ids_to_remove]
        if not session.in_transaction():
            session.commit()
