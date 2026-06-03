from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user, get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.schemas.vacancy_schema import FindVacancyResult, FindVacancy, VacancyResponse, Vacancy, VacancyCreate, VacancyUpdate
from app.services.vacancy_service import VacancyService

router = APIRouter(
    prefix="/vacancy", 
    tags=["vacancy"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindVacancyResult)
@inject
async def get_vacancy_list(
    find_query: FindVacancy = Depends(),
    service: VacancyService = Depends(Provide[Container.vacancy_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_list(find_query)


@router.get("/{vacancy_id}", response_model=VacancyResponse)
@inject
async def get_vacancy(
    vacancy_id: int,
    service: VacancyService = Depends(Provide[Container.vacancy_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_by_id(vacancy_id)


@router.post("", response_model=Vacancy)
@inject
async def create_vacancy(
    vacancy: VacancyCreate,
    service: VacancyService = Depends(Provide[Container.vacancy_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(vacancy)


@router.patch("/{vacancy_id}", response_model=Vacancy)
@inject
async def update_vacancy(
    vacancy_id: int,
    vacancy: VacancyUpdate,
    service: VacancyService = Depends(Provide[Container.vacancy_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(vacancy_id, vacancy)



@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_vacancy(
    vacancy_id: int,
    service: VacancyService = Depends(Provide[Container.vacancy_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(vacancy_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа
