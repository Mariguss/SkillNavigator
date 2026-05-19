from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.company import router as company_router
from app.api.v1.endpoints.vacancy import router as vacancy_router
from app.api.v1.endpoints.application import router as application_router

routers = APIRouter()

# Подключаем каждый роутер отдельно, сразу задавая ему префикс и теги для Swagger
routers.include_router(auth_router, prefix="/auth", tags=["Authentication"])
routers.include_router(user_router, prefix="/users", tags=["User"])
routers.include_router(company_router, prefix="/company", tags=["Companie"])
routers.include_router(vacancy_router, prefix="/vacancy", tags=["Vacancie"])
routers.include_router(application_router, prefix="/application", tags=["Application"])