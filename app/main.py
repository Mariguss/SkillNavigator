import os
import psutil
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container

# 1. Создаем кастомные метрики Prometheus
# Gauge — тип метрики, которая может как увеличиваться, так и уменьшаться
MEMORY_USAGE_GAUGE = Gauge("app_memory_usage_bytes", "Объем потребляемой памяти процессом в байтах")
CONCURRENT_REQUESTS_GAUGE = Gauge("app_concurrent_requests_count", "Число одновременных запросов в данный момент")

def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(
        title=configs.PROJECT_NAME,
        version="1.0.0",
    )
    app.container = container

    if configs.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(v1_routers, prefix=configs.API_V1_STR)

    # 2. Настраиваем middleware для подсчета одновременных запросов и памяти
    @app.middleware("http")
    async def monitor_performance(request, call_next):
        # Увеличиваем счетчик активных запросов
        CONCURRENT_REQUESTS_GAUGE.inc()
        try:
            # Обновляем показатель памяти текущего процесса
            process = psutil.Process(os.getpid())
            MEMORY_USAGE_GAUGE.set(process.memory_info().rss)
            
            response = await call_next(request)
            return response
        finally:
            # После завершения запроса уменьшаем счетчик
            CONCURRENT_REQUESTS_GAUGE.dec()

    # 3. Инициализируем автоматический сборщик (время ответа, коды ошибок и т.д.)
    # Современная инициализация без устаревших параметров
    instrumentator = Instrumentator()
    
    # Привязываем к приложению и создаем эндпоинт /metrics
    instrumentator.instrument(app).expose(app, endpoint="/metrics")

    return app

app = create_app()