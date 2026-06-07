from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.company import router as company_router
from app.api.v1.endpoints.skill import router as skill_router
from app.api.v1.endpoints.vacancy import router as vacancy_router
from app.api.v1.endpoints.application import router as application_router
from app.api.v1.endpoints.user_skills import router as user_skills_router

routers = APIRouter()

routers.include_router(auth_router)
routers.include_router(user_router)
routers.include_router(company_router)
routers.include_router(skill_router)
routers.include_router(vacancy_router)
routers.include_router(application_router)
routers.include_router(user_skills_router)

