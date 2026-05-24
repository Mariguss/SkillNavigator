from dependency_injector import containers, providers

from app.core.database import db_instance
from app.repository.company_repository import CompanyRepository
from app.repository.user_repository import UserRepository
from app.services.company_service import CompanyService
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    # Указываем модули, куда dependency_injector будет внедрять зависимости
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
            "app.api.v1.endpoints.company",
            "app.core.dependencies",
        ]
    )

    # Фабрика сессий базы данных (передаем метод session_factory из db_instance)
    session_factory = providers.Object(db_instance._session_factory)

    # Репозитории
    user_repository = providers.Factory(
        UserRepository,
        session_factory=session_factory,
    )

    company_repository = providers.Factory(
        CompanyRepository,
        session_factory=session_factory,
    )

    # Сервисы
    user_service = providers.Factory(
        UserService,
        repository=user_repository,
    )

    auth_service = providers.Factory(
        AuthService,
        repository=user_repository,
    )

    company_service = providers.Factory(
        CompanyService,
        repository=company_repository,
    )