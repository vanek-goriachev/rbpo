import uuid

from app.domain.interfaces.storage.post import PostRepository as PostRepositoryInterface
from app.domain.models.errors.domain import NotFoundError
from app.domain.models.post import Post
from app.domain.models.post_tag import PostTag


class MemoryPostStorage(PostRepositoryInterface):

    posts: dict[uuid.UUID, Post]

    def create_post(self, post: Post) -> None:
        self.posts[post.id_] = post

    def get_post_by_id(self, id_: uuid.UUID) -> Post:
        if id_ not in self.posts:
            raise NotFoundError(instance_type=Post)

        return self.posts[id_]

    def list_posts_by_filters(self, *args, **kwargs) -> list[Post]:
        return list(self.posts.values())

    def update_post(self, post: Post) -> None:
        self.posts[post.id_] = post

    def delete_post_by_id(self, id_: uuid.UUID) -> None:
        del self.posts[id_]

    def add_tag(self, id_: uuid.UUID, tag: PostTag) -> None:
        self.posts[id_].tags.append(tag)

    def remove_tag(self, id_: uuid.UUID, tag: PostTag) -> None:
        self.posts[id_].tags.remove(tag)
