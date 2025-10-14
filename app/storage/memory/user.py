import uuid

from app.domain.interfaces.storage.user import UserRepository as UserRepositoryInterface
from app.domain.models.errors.domain import NotFoundError
from app.domain.models.user import User


class UserRepository(UserRepositoryInterface):
    users: dict[uuid.UUID, User] = {}

    def get_user_by_id(self, id_: uuid.UUID) -> User:
        if id_ not in self.users:
            raise NotFoundError(instance_type=User)

        return self.users[id_]
