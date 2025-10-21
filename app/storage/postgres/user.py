import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.interfaces.storage.user import UserRepository as UserRepositoryInterface
from app.domain.models.errors.domain import AlreadyExistsError, NotFoundError
from app.domain.models.user import User
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.models import UserModel


class UserRepository(UserRepositoryInterface):
    """PostgreSQL репозиторий для пользователей"""

    def __init__(self, db_manager: DatabaseManager):
        self._db_manager = db_manager

    def get_user_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> User:
        """Получить пользователя по ID"""
        if session is not None:
            return self._get_user_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._get_user_by_id_with_session(session, id_)

    def _get_user_by_id_with_session(self, session: Session, id_: uuid.UUID) -> User:
        """Внутренний метод для получения пользователя по ID"""
        user_model = session.query(UserModel).filter(UserModel.id == id_).first()

        if not user_model:
            raise NotFoundError(instance_type=User)

        return User(id_=user_model.id, username=user_model.username)

    def create_user(self, user: User, session: Optional[Session] = None) -> None:
        """Создать нового пользователя"""
        if session is not None:
            return self._create_user_with_session(session, user)

        with self._db_manager.get_session() as session:
            return self._create_user_with_session(session, user)

    def _create_user_with_session(self, session: Session, user: User) -> None:
        """Внутренний метод для создания пользователя"""
        user_model = UserModel(id=user.id_, username=user.username)

        try:
            session.add(user_model)
            if not session.in_transaction():
                session.commit()
        except IntegrityError:
            if not session.in_transaction():
                session.rollback()
            raise AlreadyExistsError(
                instance_type=User, field_name="username", field_value=user.username
            )

    def update_user(self, user: User, session: Optional[Session] = None) -> None:
        """Обновить пользователя"""
        if session is not None:
            return self._update_user_with_session(session, user)

        with self._db_manager.get_session() as session:
            return self._update_user_with_session(session, user)

    def _update_user_with_session(self, session: Session, user: User) -> None:
        """Внутренний метод для обновления пользователя"""
        user_model = session.query(UserModel).filter(UserModel.id == user.id_).first()

        if not user_model:
            raise NotFoundError(instance_type=User)

        try:
            user_model.username = user.username
            if not session.in_transaction():
                session.commit()
        except IntegrityError:
            if not session.in_transaction():
                session.rollback()
            raise AlreadyExistsError(
                instance_type=User, field_name="username", field_value=user.username
            )

    def delete_user_by_id(self, id_: uuid.UUID, session: Optional[Session] = None) -> None:
        """Удалить пользователя по ID"""
        if session is not None:
            return self._delete_user_by_id_with_session(session, id_)

        with self._db_manager.get_session() as session:
            return self._delete_user_by_id_with_session(session, id_)

    def _delete_user_by_id_with_session(self, session: Session, id_: uuid.UUID) -> None:
        """Внутренний метод для удаления пользователя"""
        user_model = session.query(UserModel).filter(UserModel.id == id_).first()

        if not user_model:
            raise NotFoundError(instance_type=User)

        session.delete(user_model)
        if not session.in_transaction():
            session.commit()

    def get_user_by_username(
        self, username: str, session: Optional[Session] = None
    ) -> Optional[User]:
        """Получить пользователя по username"""
        if session is not None:
            return self._get_user_by_username_with_session(session, username)

        with self._db_manager.get_session() as session:
            return self._get_user_by_username_with_session(session, username)

    def _get_user_by_username_with_session(self, session: Session, username: str) -> Optional[User]:
        """Внутренний метод для получения пользователя по username"""
        user_model = session.query(UserModel).filter(UserModel.username == username).first()

        if not user_model:
            return None

        return User(id_=user_model.id, username=user_model.username)
