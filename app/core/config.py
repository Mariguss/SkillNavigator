import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

# Считываем текущую среду (по умолчанию "dev")
ENV: str = os.getenv("ENV", "dev")

class Configs(BaseSettings):
    # base
    ENV: str = ENV
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    # API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "skillnavigator"
    
    ENV_DATABASE_MAPPER: dict = {
        "prod": "fca",
        "stage": "stage-fca",
        "dev": "dev-fca",
        "test": "test-fca",
    }
    
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "sqlite": "sqlite",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    # CORS
    # BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # database
    DB: str = os.getenv("DB", "sqlite")
    DB_USER: str | None = os.getenv("DB_USER")
    DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
    DB_HOST: str | None = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    # Свойство (property) динамически соберет правильный URI в зависимости от выбранной БД
    @property
    def DATABASE_URI(self) -> str:
        if self.DB == "sqlite":
            return "sqlite:///./test.db"
        
        db_engine = self.DB_ENGINE_MAPPER.get(self.DB, "postgresql")
        return f"{db_engine}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.ENV_DATABASE_MAPPER[self.ENV]}"

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING : str= "-id"

    model_config: SettingsConfigDict = SettingsConfigDict(case_sensitive=True)


class TestConfigs(Configs):
    ENV: str = "test"
    DB: str = "sqlite"

# Инициализация объекта конфигурации
if ENV == "test":
    configs = TestConfigs()
else:
    configs = Configs()
