import uuid
from datetime import datetime as Datetime

from app.domain.models.tag import Tag


class Post:
    id_: uuid.UUID
    title: str
    text: str
    created_at: Datetime
    updated_at: Datetime
    tags: list[Tag]
