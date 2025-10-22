import uuid
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.interfaces.storage.post_tag import PostTagRepository as PostTagRepositoryInterface
from app.domain.models.errors.domain import AlreadyExistsError, NotFoundError
from app.domain.models.post_tag import PostTag
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.models import PostTagModel


class PostTagRepository(PostTagRepositoryInterface):
    """PostgreSQL репозиторий для тегов постов"""

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def create_post_tag(self, post_tag: PostTag, session: Optional[Session] = None) -> None:
        """Создать новый тег"""
        if session is not None:
            return self._create_post_tag_with_session(session, post_tag)

        with self._db_manager.get_session() as session:
            return self._create_post_tag_with_session(session, post_tag)

    def _create_post_tag_with_session(self, session: Session, post_tag: PostTag) -> None:
        """Внутренний метод для создания тега"""
        post_tag_model = PostTagModel(id=post_tag.id_, name=post_tag.name)

        try:
            session.add(post_tag_model)
            if not session.in_transaction():
                session.commit()
        except IntegrityError:
            if not session.in_transaction():
                session.rollback()
            raise AlreadyExistsError(
                instance_type=PostTag, field_name="name", field_value=post_tag.name
            )

    def get_post_tag_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> PostTag:
        """Получить тег по ID"""
        if session is not None:
            return self._get_post_tag_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._get_post_tag_by_id_with_session(session, id_)

    def _get_post_tag_by_id_with_session(self, session: Session, id_: uuid.UUID) -> PostTag:
        """Внутренний метод для получения тега по ID"""
        post_tag_model = session.query(PostTagModel).filter(PostTagModel.id == id_).first()

        if not post_tag_model:
            raise NotFoundError(instance_type=PostTag)

        return PostTag(id_=post_tag_model.id, name=post_tag_model.name)

    def update_post_tag(self, post_tag: PostTag, session: Optional[Session] = None) -> None:
        """Обновить тег"""
        if session is not None:
            return self._update_post_tag_with_session(session, post_tag)

        with self._db_manager.get_session() as session:
            return self._update_post_tag_with_session(session, post_tag)

    def _update_post_tag_with_session(self, session: Session, post_tag: PostTag) -> None:
        """Внутренний метод для обновления тега"""
        post_tag_model = session.query(PostTagModel).filter(PostTagModel.id == post_tag.id_).first()

        if not post_tag_model:
            raise NotFoundError(instance_type=PostTag)

        try:
            post_tag_model.name = post_tag.name
            if not session.in_transaction():
                session.commit()
        except IntegrityError:
            if not session.in_transaction():
                session.rollback()
            raise AlreadyExistsError(
                instance_type=PostTag, field_name="name", field_value=post_tag.name
            )

    def list_post_tags_by_filters(self, *args, **kwargs) -> List[PostTag]:
        """Получить список тегов с фильтрацией"""
        with self._db_manager.get_session() as session:
            query = session.query(PostTagModel)

            # Применяем фильтры
            if "name_contains" in kwargs:
                query = query.filter(PostTagModel.name.contains(kwargs["name_contains"]))

            if "name" in kwargs:
                query = query.filter(PostTagModel.name == kwargs["name"])

            # Сортировка
            order_by = kwargs.get("order_by", "name")
            order_direction = kwargs.get("order_direction", "asc")

            if order_direction == "desc":
                query = query.order_by(getattr(PostTagModel, order_by).desc())
            else:
                query = query.order_by(getattr(PostTagModel, order_by).asc())

            # Пагинация
            limit = kwargs.get("limit")
            offset = kwargs.get("offset", 0)

            if limit:
                query = query.limit(limit).offset(offset)

            post_tag_models = query.all()

            # Преобразуем в доменные объекты
            return [
                PostTag(id_=post_tag_model.id, name=post_tag_model.name)
                for post_tag_model in post_tag_models
            ]

    def delete_post_tag_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> None:
        """Удалить тег по ID"""
        if session is not None:
            return self._delete_post_tag_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._delete_post_tag_by_id_with_session(session, id_)

    def _delete_post_tag_by_id_with_session(self, session: Session, id_: uuid.UUID) -> None:
        """Внутренний метод для удаления тега"""
        post_tag_model = session.query(PostTagModel).filter(PostTagModel.id == id_).first()

        if not post_tag_model:
            raise NotFoundError(instance_type=PostTag)

        session.delete(post_tag_model)
        if not session.in_transaction():
            session.commit()

    def get_post_tag_by_name(
        self, name: str, session: Optional[Session] = None
    ) -> Optional[PostTag]:
        """Получить тег по имени"""
        if session is not None:
            return self._get_post_tag_by_name_with_session(session, name)

        with self._db_manager.get_session() as session:
            return self._get_post_tag_by_name_with_session(session, name)

    def _get_post_tag_by_name_with_session(self, session: Session, name: str) -> Optional[PostTag]:
        """Внутренний метод для получения тега по имени"""
        post_tag_model = session.query(PostTagModel).filter(PostTagModel.name == name).first()

        if not post_tag_model:
            return None

        return PostTag(id_=post_tag_model.id, name=post_tag_model.name)

    def get_or_create_post_tag(self, name: str, session: Optional[Session] = None) -> PostTag:
        """Получить существующий тег или создать новый"""
        existing_tag = self.get_post_tag_by_name(name, session)
        if existing_tag:
            return existing_tag

        # Создаем новый тег
        new_tag = PostTag(id_=uuid.uuid4(), name=name)
        self.create_post_tag(new_tag, session)
        return new_tag
