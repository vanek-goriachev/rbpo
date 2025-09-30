import uuid
from datetime import datetime as Datetime

from app.domain.models.post_tag import PostTag

POST_STATUS_DRAFT = "draft"
POST_STATUS_ON_MODERATION = "on_moderation"
POST_STATUS_PUBLIC = "public"
POST_STATUS_ARCHIVE = "archive"

_allowed_statuses = [
    POST_STATUS_DRAFT,
    POST_STATUS_ON_MODERATION,
    POST_STATUS_PUBLIC,
    POST_STATUS_ARCHIVE,
]


class Post:
    id_: uuid.UUID
    title: str
    body: str
    status: str
    created_at: Datetime
    updated_at: Datetime
    tags: list[PostTag] | None

    def __init__(
        self,
        id_: uuid.UUID,
        title: str,
        body: str,
        status: str,
        created_at: Datetime,
        updated_at: Datetime,
        tags: list[PostTag] = None,
    ):
        self.id_ = id_
        self.title = title
        self.body = body
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.tags = tags
