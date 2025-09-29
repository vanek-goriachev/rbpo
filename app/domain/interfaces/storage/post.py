import abc
import uuid

from app.domain.models.post import Post


class PostRepository(abc.ABC):
    @abc.abstractmethod
    def create_post(self, post: Post) -> None:
        pass

    @abc.abstractmethod
    def get_post_by_id(self, id_: uuid.UUID) -> Post:
        pass

    @abc.abstractmethod
    def update_post(self, post: Post) -> None:
        pass

    @abc.abstractmethod
    def list_posts_by_filters(self, *args, **kwargs) -> list[Post]:
        pass

    @abc.abstractmethod
    def delete_post_by_id(self, id_: uuid.UUID) -> None:
        pass
