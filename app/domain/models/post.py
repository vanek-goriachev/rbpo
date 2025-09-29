import uuid
from datetime import datetime as Datetime

from app.domain.models.tag import Tag

POST_STATUS_DRAFT = "draft"
POST_STATUS_ON_MODERATION = "on_moderation"
POST_STATUS_PUBLIC = "public"
POST_STATUS_ARCHIVE = "archive"


class Post:
    id_: uuid.UUID
    title: str
    body: str
    status: str
    created_at: Datetime
    updated_at: Datetime
    tags: list[Tag]
