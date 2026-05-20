from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container

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

    return app

app = create_app()