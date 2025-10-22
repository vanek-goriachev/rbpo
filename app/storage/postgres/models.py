import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.storage.postgres.db import Base

# Таблица для связи many-to-many между постами и тегами
post_tag_association = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", UUID(as_uuid=True), primary_key=True),
    Column("post_tag_id", UUID(as_uuid=True), primary_key=True),
)


class UserModel(Base):
    """SQLAlchemy модель для пользователей"""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PostModel(Base):
    """SQLAlchemy модель для постов"""

    __tablename__ = "posts"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с тегами через промежуточную таблицу
    tags = relationship("PostTagModel", secondary=post_tag_association, back_populates="posts")


class PostTagModel(Base):
    """SQLAlchemy модель для тегов постов"""

    __tablename__ = "post_tags"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с постами через промежуточную таблицу
    posts = relationship("PostModel", secondary=post_tag_association, back_populates="tags")
