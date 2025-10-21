"""
Unit тесты для PostgreSQL репозиториев
"""

import uuid
from datetime import datetime
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.domain.models.errors.domain import NotFoundError
from app.domain.models.post import Post
from app.domain.models.post_tag import PostTag
from app.domain.models.user import User
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.post import PostRepository
from app.storage.postgres.post_tag import PostTagRepository
from app.storage.postgres.user import UserRepository


class TestUserRepository:
    """Тесты для UserRepository"""

    @pytest.fixture
    def mock_db_manager(self):
        """Мок для DatabaseManager"""
        return Mock(spec=DatabaseManager)

    @pytest.fixture
    def mock_session(self):
        """Мок для SQLAlchemy Session"""
        return Mock(spec=Session)

    @pytest.fixture
    def user_repo(self, mock_db_manager):
        """Экземпляр UserRepository"""
        return UserRepository(mock_db_manager)

    @pytest.fixture
    def sample_user(self):
        """Образец пользователя"""
        return User(id_=uuid.uuid4(), username="test_user")

    def test_create_user_success(self, user_repo, mock_db_manager, mock_session, sample_user):
        """Тест успешного создания пользователя"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.in_transaction.return_value = False

        # Выполнение
        user_repo.create_user(sample_user)

        # Проверки
        mock_db_manager.get_session.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_create_user_with_session(self, user_repo, mock_session, sample_user):
        """Тест создания пользователя с внешней сессией"""
        # Настройка моков
        mock_session.in_transaction.return_value = True

        # Выполнение
        user_repo.create_user(sample_user, mock_session)

        # Проверки
        mock_session.add.assert_called_once()
        mock_session.commit.assert_not_called()  # Не коммитим, так как в транзакции

    def test_get_user_by_id_success(self, user_repo, mock_db_manager, mock_session, sample_user):
        """Тест успешного получения пользователя по ID"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_user_model = Mock()
        mock_user_model.id = sample_user.id_
        mock_user_model.username = sample_user.username
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user_model

        # Выполнение
        result = user_repo.get_user_by_id(sample_user.id_)

        # Проверки
        assert result.id_ == sample_user.id_
        assert result.username == sample_user.username
        mock_db_manager.get_session.assert_called_once()

    def test_get_user_by_id_not_found(self, user_repo, mock_db_manager, mock_session):
        """Тест получения несуществующего пользователя"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Выполнение и проверка исключения
        with pytest.raises(NotFoundError):
            user_repo.get_user_by_id(uuid.uuid4())

    def test_update_user_success(self, user_repo, mock_db_manager, mock_session, sample_user):
        """Тест успешного обновления пользователя"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_user_model = Mock()
        mock_user_model.id = sample_user.id_
        mock_user_model.username = sample_user.username
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user_model
        mock_session.in_transaction.return_value = False

        # Выполнение
        user_repo.update_user(sample_user)

        # Проверки
        assert mock_user_model.username == sample_user.username
        mock_session.commit.assert_called_once()

    def test_delete_user_success(self, user_repo, mock_db_manager, mock_session, sample_user):
        """Тест успешного удаления пользователя"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_user_model = Mock()
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user_model
        mock_session.in_transaction.return_value = False

        # Выполнение
        user_repo.delete_user_by_id(sample_user.id_)

        # Проверки
        mock_session.delete.assert_called_once_with(mock_user_model)
        mock_session.commit.assert_called_once()


class TestPostRepository:
    """Тесты для PostRepository"""

    @pytest.fixture
    def mock_db_manager(self):
        """Мок для DatabaseManager"""
        return Mock(spec=DatabaseManager)

    @pytest.fixture
    def mock_session(self):
        """Мок для SQLAlchemy Session"""
        return Mock(spec=Session)

    @pytest.fixture
    def post_repo(self, mock_db_manager):
        """Экземпляр PostRepository"""
        return PostRepository(mock_db_manager)

    @pytest.fixture
    def sample_post(self):
        """Образец поста"""
        return Post(
            id_=uuid.uuid4(),
            title="Test Post",
            body="Test body",
            status="draft",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def test_create_post_success(self, post_repo, mock_db_manager, mock_session, sample_post):
        """Тест успешного создания поста"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.in_transaction.return_value = False

        # Выполнение
        post_repo.create_post(sample_post)

        # Проверки
        mock_db_manager.get_session.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_get_post_by_id_success(self, post_repo, mock_db_manager, mock_session, sample_post):
        """Тест успешного получения поста по ID"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_post_model = Mock()
        mock_post_model.id = sample_post.id_
        mock_post_model.title = sample_post.title
        mock_post_model.body = sample_post.body
        mock_post_model.status = sample_post.status
        mock_post_model.created_at = sample_post.created_at
        mock_post_model.updated_at = sample_post.updated_at
        mock_post_model.tags = []
        mock_session.query.return_value.filter.return_value.first.return_value = mock_post_model

        # Выполнение
        result = post_repo.get_post_by_id(sample_post.id_)

        # Проверки
        assert result.id_ == sample_post.id_
        assert result.title == sample_post.title
        assert result.body == sample_post.body
        assert result.status == sample_post.status

    def test_get_post_by_id_not_found(self, post_repo, mock_db_manager, mock_session):
        """Тест получения несуществующего поста"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Выполнение и проверка исключения
        with pytest.raises(NotFoundError):
            post_repo.get_post_by_id(uuid.uuid4())


class TestPostTagRepository:
    """Тесты для PostTagRepository"""

    @pytest.fixture
    def mock_db_manager(self):
        """Мок для DatabaseManager"""
        return Mock(spec=DatabaseManager)

    @pytest.fixture
    def mock_session(self):
        """Мок для SQLAlchemy Session"""
        return Mock(spec=Session)

    @pytest.fixture
    def post_tag_repo(self, mock_db_manager):
        """Экземпляр PostTagRepository"""
        return PostTagRepository(mock_db_manager)

    @pytest.fixture
    def sample_post_tag(self):
        """Образец тега"""
        return PostTag(id_=uuid.uuid4(), name="test_tag")

    def test_create_post_tag_success(
        self, post_tag_repo, mock_db_manager, mock_session, sample_post_tag
    ):
        """Тест успешного создания тега"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.in_transaction.return_value = False

        # Выполнение
        post_tag_repo.create_post_tag(sample_post_tag)

        # Проверки
        mock_db_manager.get_session.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_get_post_tag_by_id_success(
        self, post_tag_repo, mock_db_manager, mock_session, sample_post_tag
    ):
        """Тест успешного получения тега по ID"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_tag_model = Mock()
        mock_tag_model.id = sample_post_tag.id_
        mock_tag_model.name = sample_post_tag.name
        mock_session.query.return_value.filter.return_value.first.return_value = mock_tag_model

        # Выполнение
        result = post_tag_repo.get_post_tag_by_id(sample_post_tag.id_)

        # Проверки
        assert result.id_ == sample_post_tag.id_
        assert result.name == sample_post_tag.name

    def test_get_post_tag_by_id_not_found(self, post_tag_repo, mock_db_manager, mock_session):
        """Тест получения несуществующего тега"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = None

        # Выполнение и проверка исключения
        with pytest.raises(NotFoundError):
            post_tag_repo.get_post_tag_by_id(uuid.uuid4())

    def test_get_or_create_post_tag_existing(
        self, post_tag_repo, mock_db_manager, mock_session, sample_post_tag
    ):
        """Тест получения существующего тега"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_tag_model = Mock()
        mock_tag_model.id = sample_post_tag.id_
        mock_tag_model.name = sample_post_tag.name
        mock_session.query.return_value.filter.return_value.first.return_value = mock_tag_model

        # Выполнение
        result = post_tag_repo.get_or_create_post_tag(sample_post_tag.name)

        # Проверки
        assert result.id_ == sample_post_tag.id_
        assert result.name == sample_post_tag.name
        mock_session.add.assert_not_called()  # Тег не создавался

    def test_get_or_create_post_tag_new(self, post_tag_repo, mock_db_manager, mock_session):
        """Тест создания нового тега"""
        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.query.return_value.filter.return_value.first.return_value = (
            None  # Тег не найден
        )
        mock_session.in_transaction.return_value = False

        # Выполнение
        result = post_tag_repo.get_or_create_post_tag("new_tag")

        # Проверки
        assert result.name == "new_tag"
        mock_session.add.assert_called_once()  # Тег был создан
        mock_session.commit.assert_called_once()
