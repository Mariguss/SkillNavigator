from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.schemas.analytics_schema import UserFunnelResponse, ApplicationStatsResponse
from app.schemas.vacancy_schema import FindVacancy
from app.schemas.company_schema import FindCompany
from app.services.analytics_service import AnalyticsService
from app.repository.user_skills_repository import UserSkillsRepository
from app.repository.vacancy_skills_repository import VacancySkillsRepository
from app.repository.vacancy_repository import VacancyRepository
from app.repository.company_repository import CompanyRepository

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    dependencies=[Depends(JWTBearer())],
)


@router.get("/funnel", response_model=UserFunnelResponse)
@inject
async def get_my_funnel(
    current_user: User = Depends(get_current_user),
    analytics_service: AnalyticsService = Depends(Provide[Container.analytics_service]),
):
    return analytics_service.get_user_funnel(current_user.id)


@router.get("/stats", response_model=ApplicationStatsResponse)
@inject
async def get_my_stats(
    current_user: User = Depends(get_current_user),
    analytics_service: AnalyticsService = Depends(Provide[Container.analytics_service]),
):
    return analytics_service.get_application_stats(current_user.id)


@router.get("/top-skills")
@inject
async def get_top_skills(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    analytics_service: AnalyticsService = Depends(Provide[Container.analytics_service]),
):
    return analytics_service.get_top_skills(limit=limit)


@router.get("/vacancy-dynamics")
@inject
async def get_vacancy_dynamics(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    analytics_service: AnalyticsService = Depends(Provide[Container.analytics_service]),
):
    return analytics_service.get_vacancy_dynamics(days=days)


@router.get("/vacancy-matches")
@inject
async def get_vacancy_matches(
    min_match: float = 0,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    user_skills_repo: UserSkillsRepository = Depends(Provide[Container.user_skills_repository]),
    vacancy_repo: VacancyRepository = Depends(Provide[Container.vacancy_repository]),
    vacancy_skills_repo: VacancySkillsRepository = Depends(Provide[Container.vacancy_skills_repository]),
    company_repo: CompanyRepository = Depends(Provide[Container.company_repository]),
):
    user_skill_ids = user_skills_repo.get_skill_ids(current_user.id)

    # Все активные вакансии
    result = vacancy_repo.read_by_options(FindVacancy(is_active__eq=True, page_size="all"))
    vacancies = result["founds"]

    # Кеш компаний id -> name
    company_cache: dict[int, str] = {}
    companies = company_repo.read_by_options(FindCompany(page_size="all"))["founds"]
    for c in companies:
        company_cache[c.id] = c.name

    matches = []
    for v in vacancies:
        v_skill_ids = vacancy_skills_repo.get_skill_ids(v.id)
        if not v_skill_ids:
            continue

        if user_skill_ids:
            matched = user_skill_ids & v_skill_ids
            pct = round(len(matched) / len(v_skill_ids) * 100, 1)
        else:
            matched = set()
            pct = 0.0

        if pct < min_match:
            continue

        matches.append({
            "vacancy_id": v.id,
            "title": v.title,
            "company_id": v.company_id,
            "company_name": company_cache.get(v.company_id, f"Компания #{v.company_id}"),
            "url": v.url,
            "match_percent": pct,
            "matched_count": len(matched),
            "total_skill_count": len(v_skill_ids),
        })

    matches.sort(key=lambda x: x["match_percent"], reverse=True)
    total = len(matches)
    start = (page - 1) * page_size
    return {
        "matches": matches[start: start + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
        "user_skill_count": len(user_skill_ids),
    }
