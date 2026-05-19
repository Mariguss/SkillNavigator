from app.models.base_model import Base
from app.models.application import Application
from app.models.company import Company
from app.models.skill import Skill
from app.models.user_skills import UserSkills
from app.models.user import User
from app.models.vacancy_skills import VacancySkills
from app.models.vacancy import Vacancy

# Перечисляем все модели, чтобы их было удобно импортировать
__all__ = [
    "Base",
    "Application",
    "Company",
    "Skill",
    "UserSkills",
    "User",
    "VacancySkills",
    "Vacancy",
]
