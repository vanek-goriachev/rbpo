from contextlib import contextmanager
from typing import Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import IsolationLevel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


class DatabaseManager:
    """Менеджер для работы с базой данных PostgreSQL"""

    def __init__(self):
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._initialized = False

    def initialize(
        self, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str
    ) -> None:
        """Инициализация подключения к базе данных"""
        if self._initialized:
            return

        # Создаем URL подключения
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        # Создаем движок
        self._engine = create_engine(
            database_url,
            echo=False,  # Установите True для отладки SQL запросов
            pool_pre_ping=True,  # Проверка соединения перед использованием
            pool_recycle=3600,  # Переподключение каждый час
        )

        # Создаем фабрику сессий
        self._session_factory = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)

        self._initialized = True

    @property
    def engine(self) -> Engine:
        """Получить движок базы данных"""
        if not self._initialized:
            raise RuntimeError("DatabaseManager не инициализирован. Вызовите initialize() сначала.")
        return self._engine

    @contextmanager
    def get_session(self) -> Session:
        """Контекстный менеджер для получения сессии БД"""
        if not self._initialized:
            raise RuntimeError("DatabaseManager не инициализирован. Вызовите initialize() сначала.")

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self) -> None:
        """Создание всех таблиц в базе данных"""
        if not self._initialized:
            raise RuntimeError("DatabaseManager не инициализирован. Вызовите initialize() сначала.")
        Base.metadata.create_all(bind=self._engine)

    def drop_tables(self) -> None:
        """Удаление всех таблиц из базы данных"""
        if not self._initialized:
            raise RuntimeError("DatabaseManager не инициализирован. Вызовите initialize() сначала.")
        Base.metadata.drop_all(bind=self._engine)

    @contextmanager
    def transaction(self, isolation_level: IsolationLevel = None):
        """Контекстный менеджер для транзакций с возможностью задания уровня изоляции"""
        if not self._initialized:
            raise RuntimeError("DatabaseManager не инициализирован. Вызовите initialize() сначала.")

        session = self._session_factory()
        try:
            if isolation_level:
                session.connection().connection.set_isolation_level(isolation_level)

            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
