from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.services.user_skills_service import UserSkillsService


class AddSkillRequest(BaseModel):
    skill_id: int


router = APIRouter(
    prefix="/me/skills",
    tags=["user-skills"],
    dependencies=[Depends(JWTBearer())],
)


@router.get("")
@inject
async def get_my_skills(
    current_user: User = Depends(get_current_user),
    service: UserSkillsService = Depends(Provide[Container.user_skills_service]),
):
    return service.get_skills(current_user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def add_my_skill(
    body: AddSkillRequest,
    current_user: User = Depends(get_current_user),
    service: UserSkillsService = Depends(Provide[Container.user_skills_service]),
):
    return service.add_skill(current_user.id, body.skill_id)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_my_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    service: UserSkillsService = Depends(Provide[Container.user_skills_service]),
):
    service.remove_skill(current_user.id, skill_id)
    return None
