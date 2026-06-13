import os
import asyncio
import psutil
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Gauge

from app.api.v1.routes import routers as v1_routers
from app.api.pages import router as pages_router
from app.core.config import configs
from app.core.container import Container

MEMORY_USAGE_GAUGE = Gauge("app_memory_usage_bytes", "Объем потребляемой памяти процессом в байтах")
CONCURRENT_REQUESTS_GAUGE = Gauge("app_concurrent_requests_count", "Число одновременных запросов в данный момент")


async def _hygiene_loop(container: Container):
    while True:
        try:
            await asyncio.sleep(60*60)  # раз в сутки 60 * 60 * 24 
            hygiene_service = container.hygiene_service()
            hygiene_service.archive_old_vacancies(days=3)
        except asyncio.CancelledError:
            break
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Связываем AIService с ParserService (фоновое извлечение навыков)
    parser_svc = app.container.parser_service()
    ai_svc = app.container.ai_service()
    parser_svc.set_ai_service(ai_svc)

    hygiene_task = asyncio.create_task(_hygiene_loop(app.container))
    yield
    # Stop parser scheduler if running
    try:
        scheduler = app.container.parser_scheduler()
        scheduler.stop()
    except Exception:
        pass
    hygiene_task.cancel()
    try:
        await hygiene_task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(
        title=configs.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan,
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

    # HTML pages at root
    app.include_router(pages_router)
    # API endpoints
    app.include_router(v1_routers, prefix=configs.API_V1_STR)

    @app.middleware("http")
    async def monitor_performance(request, call_next):
        CONCURRENT_REQUESTS_GAUGE.inc()
        try:
            process = psutil.Process(os.getpid())
            MEMORY_USAGE_GAUGE.set(process.memory_info().rss)
            response = await call_next(request)
            return response
        finally:
            CONCURRENT_REQUESTS_GAUGE.dec()

    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app, endpoint="/metrics")

    return app


app = create_app()
