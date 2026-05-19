from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from models.base_model import Base

class Database:
    def __init__(self, db_url: str) -> None:

        # Для SQLite добавляем check_same_thread=False, для остальных БД это проигнорируется
        connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

        self._engine = create_engine(db_url, echo=True, connect_args=connect_args)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        """Создает таблицы. Удобно для локальных тестов."""
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Контекстный менеджер сессии для использования в обычных Python-скриптах/сервисах."""

        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


from app.core.config import configs

# Создаем единственный экземпляр класса Database
db_instance = Database(configs.DATABASE_URI)

# Эта функция будет выдавать сессию для каждого запроса API
def get_db():
    """Отдает сессию в роуты FastAPI и правильно закрывает её после ответа сервера."""
    
    # Используем фабрику напрямую, чтобы FastAPI сам контролировал жизненный цикл
    db = db_instance._session_factory()
    try:
        yield db
    finally:
        db.close()
