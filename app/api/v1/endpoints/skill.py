from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user, get_current_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.schemas.skill_schema import SkillResponse, SkillUpdate, FindSkillResult, FindSkill, SkillCreate, Skill
from app.services.skill_service import SkillService

router = APIRouter(
    prefix="/skill", 
    tags=["skill"]
)

_auth = [Depends(JWTBearer())]

@router.get("", response_model=FindSkillResult)
@inject
async def get_skill_list(
    find_query: FindSkill = Depends(),
    service: SkillService = Depends(Provide[Container.skill_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_list(find_query)


@router.get("/{skill_id}", response_model=SkillResponse)
@inject
async def get_skill(
    skill_id: int,
    service: SkillService = Depends(Provide[Container.skill_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_by_id(skill_id)


@router.post("", response_model=Skill, dependencies=_auth)
@inject
async def create_skill(
    skill: SkillCreate,
    service: SkillService = Depends(Provide[Container.skill_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(skill)


@router.patch("/{skill_id}", response_model=Skill, dependencies=_auth)
@inject
async def update_skill(
    skill_id: int,
    skill: SkillUpdate,
    service: SkillService = Depends(Provide[Container.skill_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(skill_id, skill)


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=_auth)
@inject
async def delete_skill(
    skill_id: int,
    service: SkillService = Depends(Provide[Container.skill_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(skill_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа
