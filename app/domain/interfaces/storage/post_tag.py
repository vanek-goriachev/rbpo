import abc
import uuid

from app.domain.models.post_tag import PostTag


class PostTagRepository(abc.ABC):
    @abc.abstractmethod
    def create_post_tag(self, post_tag: PostTag) -> None:
        pass

    @abc.abstractmethod
    def get_post_tag_by_id(self, id_: uuid.UUID) -> PostTag:
        pass

    @abc.abstractmethod
    def update_post_tag(self, post_tag: PostTag) -> None:
        pass

    @abc.abstractmethod
    def list_post_tags_by_filters(self, *args, **kwargs) -> list[PostTag]:
        pass

    @abc.abstractmethod
    def delete_post_tag_by_id(self, id_: uuid.UUID) -> None:
        pass
