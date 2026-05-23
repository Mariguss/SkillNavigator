from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user
from app.core.security import JWTBearer
from app.schemas.base_schema import Blank
from app.schemas.user_schema import FindUser, FindUserResult, UpsertUser, User
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user", 
    tags=["user"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindUserResult)
@inject
async def get_user_list(
    find_query: FindUser = Depends(),
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_list(find_query)


@router.get("/{user_id}", response_model=User)
@inject
async def get_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_by_id(user_id)


@router.post("", response_model=User)
@inject
async def create_user(
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(user)


@router.patch("/{user_id}", response_model=User)
@inject
async def update_user(
    user_id: int,
    user: UpsertUser,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(user_id, user)



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(user_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа
