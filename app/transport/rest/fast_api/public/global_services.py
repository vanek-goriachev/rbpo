from app.domain.services.post import PostService
from app.domain.services.post_tag import PostTagService

post_service: PostService = None
post_tag_service: PostTagService = None


def is_initialized() -> bool:
    return post_service is not None and post_tag_service is not None


def initialize(
    new_post_service: PostService,
    new_post_tag_service: PostTagService,
) -> None:
    global post_service, post_tag_service

    post_service = new_post_service
    post_tag_service = new_post_tag_service

    return
