import uuid
from datetime import datetime as DateTime

from app.domain.interfaces.storage.post import PostRepository
from app.domain.interfaces.storage.post_tag import PostTagRepository
from app.domain.models.post import Post


class PostService:
    def __init__(self, post_repository: PostRepository, post_tag_repository: PostTagRepository):
        self.post_repository = post_repository
        self.post_tag_repository = post_tag_repository

    def get_post(self, id_: uuid.UUID) -> Post:
        return self.post_repository.get_post_by_id(id_)

    def create_post(self, title: str, body: str, status: str) -> uuid.UUID:
        post = Post(
            id_=uuid.uuid4(),
            title=title,
            body=body,
            status=status,
            created_at=DateTime.now(),
            updated_at=DateTime.now(),
        )

        self.post_repository.create_post(post)

        return post.id_

    def list_posts(self) -> list[Post]:
        return self.post_repository.list_posts_by_filters()

    def update_post(self, id_: uuid.UUID, **kwargs):
        post = self.post_repository.get_post_by_id(id_)

        for key, value in kwargs.items():
            if key not in ["id_", "created_at", "updated_at"]:
                setattr(post, key, value)

        post.updated_at = DateTime.now()

        return self.post_repository.update_post(post)

    def delete_post(self, id_: uuid.UUID):
        return self.post_repository.delete_post_by_id(id_)

    def add_tags(self, id_: uuid.UUID, tags_ids: list[uuid.UUID]) -> None:
        tags = []
        for id_ in tags_ids:
            tags.append(self.post_tag_repository.get_post_tag_by_id(id_))

        self.post_repository.add_tags(id_, tags)

    def remove_tags(self, id_: uuid.UUID, tags_ids: list[uuid.UUID]) -> None:
        tags = []
        for id_ in tags_ids:
            tags.append(self.post_tag_repository.get_post_tag_by_id(id_))

        self.post_repository.remove_tags(id_, tags)
