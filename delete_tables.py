from app.core.database import db_instance
from app.models.vacancy import Vacancy
from app.models.company import Company
from app.models.skill import Skill
from app.models.vacancy_skills import VacancySkills
from app.models.user_skills import UserSkills
from app.models.application import Application

with db_instance._session_factory() as session:
    session.query(VacancySkills).delete()
    session.query(UserSkills).delete()
    session.query(Skill).delete()
    session.query(Application).delete()  

    session.query(Vacancy).delete()
    session.query(Company).delete()
    session.commit()