from app.repository.vacancy_repository import VacancyRepository


class HygieneService:
    def __init__(self, vacancy_repository: VacancyRepository) -> None:
        self.vacancy_repository = vacancy_repository

    def archive_old_vacancies(self, days: int = 90) -> dict:
        count = self.vacancy_repository.archive_old_vacancies(days=days)
        return {"archived": count, "days_threshold": days}
