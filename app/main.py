from fastapi import FastAPI
from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.database import BaseModel, create_engine

app = FastAPI(title=configs.PROJECT_NAME, version="1.0.0")

# Подключаем роутеры со всеми эндпоинтами
app.include_router(v1_routers, prefix=configs.API_V1_STR)

# Автоматическое создание таблиц при старте бэкенда
@app.on_event("startup")
def startup_event():
    # Создаем движок SQLAlchemy напрямую по нашему URI из конфигов
    engine = create_engine(configs.DATABASE_URI)
    # Команда берет класс BaseModel и создает в Postgres все таблицы, которые от него унаследованы
    BaseModel.metadata.create_all(bind=engine)