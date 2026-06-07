from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.container import Container
from app.core.dependencies import get_current_super_user
from app.core.security import JWTBearer
from app.schemas.user_schema import User
from app.services.parser_scheduler import ParserScheduler
from app.services.hygiene_service import HygieneService

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
    dependencies=[Depends(JWTBearer())],
)


@router.post("/run")
@inject
async def run_parser_once(
    current_user: User = Depends(get_current_super_user),
    scheduler: ParserScheduler = Depends(Provide[Container.parser_scheduler]),
):
    """Запустить парсер вручную (однократно)."""
    return scheduler.run_once_background()


@router.post("/start")
@inject
async def start_parser(
    interval_minutes: int = 60,
    current_user: User = Depends(get_current_super_user),
    scheduler: ParserScheduler = Depends(Provide[Container.parser_scheduler]),
):
    """Запустить парсер как фоновую задачу с заданным интервалом (в минутах)."""
    return scheduler.start(interval_minutes=interval_minutes)


@router.post("/stop")
@inject
async def stop_parser(
    current_user: User = Depends(get_current_super_user),
    scheduler: ParserScheduler = Depends(Provide[Container.parser_scheduler]),
):
    """Остановить фоновый парсер."""
    return scheduler.stop()


@router.get("/status")
@inject
async def parser_status(
    current_user: User = Depends(get_current_super_user),
    scheduler: ParserScheduler = Depends(Provide[Container.parser_scheduler]),
):
    """Статус фонового парсера."""
    return scheduler.status()


@router.post("/archive")
@inject
async def archive_old_vacancies(
    days: int = 90,
    current_user: User = Depends(get_current_super_user),
    hygiene_service: HygieneService = Depends(Provide[Container.hygiene_service]),
):
    """Архивировать вакансии старше N дней (soft delete)."""
    return hygiene_service.archive_old_vacancies(days=days)
