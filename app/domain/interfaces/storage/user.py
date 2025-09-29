import abc
import uuid

from app.domain.models.user import User


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def get_user_by_id(self, id_: uuid.UUID) -> User:
        pass
