from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user, get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.schemas.application_schema import ApplicationResponse, ApplicationUpdate, FindApplicationResult, FindApplication, ApplicationCreate, Application
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/application", 
    tags=["application"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindApplicationResult)
@inject
async def get_application_list(
    find_query: FindApplication = Depends(),
    service: ApplicationService = Depends(Provide[Container.application_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_list(find_query)


@router.get("/{application_id}", response_model=ApplicationResponse)
@inject
async def get_application(
    application_id: int,
    service: ApplicationService = Depends(Provide[Container.application_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_by_id(application_id)


@router.post("", response_model=Application)
@inject
async def create_application(
    application: ApplicationCreate,
    service: ApplicationService = Depends(Provide[Container.application_service]),
    current_user: User = Depends(get_current_user),
):
    return service.add(application)


@router.patch("/{application_id}", response_model=Application)
@inject
async def update_application(
    application_id: int,
    application: ApplicationUpdate,
    service: ApplicationService = Depends(Provide[Container.application_service]),
    current_user: User = Depends(get_current_user),
):
    return service.patch(application_id, application)



@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_application(
    application_id: int,
    service: ApplicationService = Depends(Provide[Container.application_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(application_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа
