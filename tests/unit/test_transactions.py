"""
Unit тесты для транзакций
"""

import uuid
from datetime import datetime
from unittest.mock import Mock

import pytest
from sqlalchemy.engine import IsolationLevel

from app.domain.models.post import Post
from app.domain.models.post_tag import PostTag
from app.domain.models.user import User
from app.storage.postgres.db import DatabaseManager
from app.storage.postgres.post import PostRepository
from app.storage.postgres.post_tag import PostTagRepository
from app.storage.postgres.user import UserRepository


class TestTransactionSupport:
    """Тесты для поддержки транзакций"""

    @pytest.fixture
    def mock_db_manager(self):
        """Мок для DatabaseManager"""
        db_manager = Mock(spec=DatabaseManager)
        db_manager.transaction.return_value.__enter__.return_value = Mock()
        return db_manager

    @pytest.fixture
    def mock_session(self):
        """Мок для SQLAlchemy Session"""
        session = Mock()
        session.in_transaction.return_value = True
        return session

    @pytest.fixture
    def user_repo(self, mock_db_manager):
        """Экземпляр UserRepository"""
        return UserRepository(mock_db_manager)

    @pytest.fixture
    def post_repo(self, mock_db_manager):
        """Экземпляр PostRepository"""
        return PostRepository(mock_db_manager)

    @pytest.fixture
    def post_tag_repo(self, mock_db_manager):
        """Экземпляр PostTagRepository"""
        return PostTagRepository(mock_db_manager)

    def test_user_repo_with_session(self, user_repo, mock_session):
        """Тест UserRepository с внешней сессией"""
        user = User(id_=uuid.uuid4(), username="test_user")

        # Тест создания пользователя с сессией
        user_repo.create_user(user, mock_session)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_not_called()  # В транзакции не коммитим

    def test_post_repo_with_session(self, post_repo, mock_session):
        """Тест PostRepository с внешней сессией"""
        post = Post(
            id_=uuid.uuid4(),
            title="Test Post",
            body="Test body",
            status="draft",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Тест создания поста с сессией
        post_repo.create_post(post, mock_session)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_not_called()  # В транзакции не коммитим

    def test_post_tag_repo_with_session(self, post_tag_repo, mock_session):
        """Тест PostTagRepository с внешней сессией"""
        tag = PostTag(id_=uuid.uuid4(), name="test_tag")

        # Тест создания тега с сессией
        post_tag_repo.create_post_tag(tag, mock_session)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_not_called()  # В транзакции не коммитим

    def test_transaction_isolation_levels(self, mock_db_manager):
        """Тест различных уровней изоляции транзакций"""
        # Тест READ_COMMITTED
        mock_db_manager.transaction(IsolationLevel.READ_COMMITTED)

        # Тест REPEATABLE_READ
        mock_db_manager.transaction(IsolationLevel.REPEATABLE_READ)

        # Тест SERIALIZABLE
        mock_db_manager.transaction(IsolationLevel.SERIALIZABLE)

        # Проверяем, что метод transaction вызывался с правильными параметрами
        assert mock_db_manager.transaction.call_count == 3

    def test_repository_methods_without_session(self, user_repo, mock_db_manager, mock_session):
        """Тест методов репозитория без внешней сессии"""
        user = User(id_=uuid.uuid4(), username="test_user")

        # Настройка моков
        mock_db_manager.get_session.return_value.__enter__.return_value = mock_session
        mock_session.in_transaction.return_value = False

        # Выполнение
        user_repo.create_user(user)

        # Проверки
        mock_db_manager.get_session.assert_called_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()  # Без транзакции коммитим


class TestTransactionIntegration:
    """Интеграционные тесты для транзакций"""

    @pytest.fixture
    def mock_db_manager(self):
        """Мок для DatabaseManager с поддержкой транзакций"""
        db_manager = Mock(spec=DatabaseManager)

        # Настройка контекстного менеджера для транзакций
        mock_session = Mock()
        mock_session.in_transaction.return_value = True
        db_manager.transaction.return_value.__enter__.return_value = mock_session
        db_manager.transaction.return_value.__exit__.return_value = None

        return db_manager

    @pytest.fixture
    def repositories(self, mock_db_manager):
        """Репозитории для тестирования"""
        return {
            "user": UserRepository(mock_db_manager),
            "post": PostRepository(mock_db_manager),
            "post_tag": PostTagRepository(mock_db_manager),
        }

    def test_transaction_context_manager(self, mock_db_manager):
        """Тест использования контекстного менеджера транзакций"""
        with mock_db_manager.transaction() as session:
            assert session is not None
            assert session.in_transaction.return_value is True

        # Проверяем, что контекстный менеджер был вызван
        mock_db_manager.transaction.assert_called_once()

    def test_transaction_with_isolation_level(self, mock_db_manager):
        """Тест транзакции с уровнем изоляции"""
        with mock_db_manager.transaction(IsolationLevel.SERIALIZABLE) as session:
            assert session is not None

        # Проверяем, что транзакция была создана с правильным уровнем изоляции
        mock_db_manager.transaction.assert_called_once_with(IsolationLevel.SERIALIZABLE)

    def test_multiple_operations_in_transaction(self, repositories, mock_db_manager):
        """Тест выполнения нескольких операций в одной транзакции"""
        user = User(id_=uuid.uuid4(), username="test_user")
        post = Post(
            id_=uuid.uuid4(),
            title="Test Post",
            body="Test body",
            status="draft",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        tag = PostTag(id_=uuid.uuid4(), name="test_tag")

        # Получаем сессию из контекстного менеджера
        mock_session = mock_db_manager.transaction.return_value.__enter__.return_value

        with mock_db_manager.transaction() as session:
            # Выполняем несколько операций в одной транзакции
            repositories["user"].create_user(user, session)
            repositories["post_tag"].create_post_tag(tag, session)
            repositories["post"].create_post(post, session)

        # Проверяем, что все операции использовали одну и ту же сессию
        assert mock_session.add.call_count == 3  # user, tag, post
        mock_session.commit.assert_not_called()  # В транзакции не коммитим отдельно
