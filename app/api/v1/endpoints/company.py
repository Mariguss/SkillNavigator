from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user, get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.schemas.company_schema import CompanyResponse, CompanyUpdate, FindCompanyResult, FindCompany, CompanyCreate, Company
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/company", 
    tags=["company"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindCompanyResult)
@inject
async def get_company_list(
    find_query: FindCompany = Depends(),
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_list(find_query)


@router.get("/{company_id}", response_model=CompanyResponse)
@inject
async def get_company(
    company_id: int,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_by_id(company_id)


@router.post("", response_model=Company)
@inject
async def create_company(
    company: CompanyCreate,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(company)


@router.patch("/{company_id}", response_model=Company)
@inject
async def update_company(
    company_id: int,
    company: CompanyUpdate,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(company_id, company)



@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_company(
    company_id: int,
    service: CompanyService = Depends(Provide[Container.company_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(company_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа
