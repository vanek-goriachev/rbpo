import uuid

from app.domain.interfaces.storage.post_tag import PostTagRepository as PostTagRepositoryInterface
from app.domain.models.errors.domain import NotFoundError
from app.domain.models.post_tag import PostTag


class MemoryPostTagStorage(PostTagRepositoryInterface):
    post_tags: dict[uuid.UUID, PostTag]

    def create_post_tag(self, post_tag: PostTag) -> None:
        self.post_tags[post_tag.id_] = post_tag

    def get_post_tag_by_id(self, id_: uuid.UUID) -> PostTag:
        if id_ not in self.post_tags:
            raise NotFoundError(instance_type=PostTag)
        return self.post_tags[id_]

    def update_post_tag(self, post_tag: PostTag) -> None:
        self.post_tags[post_tag.id_] = post_tag

    def list_post_tags_by_filters(self, *args, **kwargs) -> list[PostTag]:
        return list(self.post_tags.values())

    def delete_post_tag_by_id(self, id_: uuid.UUID) -> None:
        del self.post_tags[id_]
