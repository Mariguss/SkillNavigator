from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company_schema import CompanyCreate

def create_company(db: Session, company_data: CompanyCreate):
    # Создаем объект модели
    db_company = Company(name=company_data.name, site_url=company_data.site_url)
    
    db.add(db_company)      # Добавляем в транзакцию
    db.commit()             # Сохраняем в БД
    db.refresh(db_company)  # Обновляем, чтобы получить сгенерированный ID
    
    return db_company