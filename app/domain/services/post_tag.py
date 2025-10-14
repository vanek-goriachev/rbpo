import uuid

from app.domain.interfaces.storage.post_tag import PostTagRepository
from app.domain.models.post_tag import PostTag


class PostTagService:
    def __init__(self, post_tag_repository: PostTagRepository):
        self.post_tag_repository = post_tag_repository

    def get_post_tag(self, id_: uuid.UUID) -> PostTag:
        return self.post_tag_repository.get_post_tag_by_id(id_)

    def create_post_tag(self, data: dict):
        post_tag = PostTag(**data)

        post_tag.id_ = uuid.uuid4()

        return self.post_tag_repository.create_post_tag(post_tag)

    def list_post_tags(self) -> list[PostTag]:
        return self.post_tag_repository.list_post_tags_by_filters()

    def update_post_tag(self, id_: uuid.UUID, data: dict):
        post = self.post_tag_repository.get_post_tag_by_id(id_)

        for key, value in data.items():
            if key != "id_":
                setattr(post, key, value)

        return self.post_tag_repository.update_post_tag(post)

    def delete_post_tag(self, id_: uuid.UUID):
        return self.post_tag_repository.delete_post_tag_by_id(id_)
