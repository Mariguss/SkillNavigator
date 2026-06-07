from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta, timezone

from app.models.application import Application
from app.models.vacancy_skills import VacancySkills
from app.models.skill import Skill
from app.models.vacancy import Vacancy


class AnalyticsService:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_user_funnel(self, user_id: int) -> dict:
        with self.session_factory() as session:
            apps = session.query(Application).filter(Application.user_id == user_id).all()
        if not apps:
            return {"funnel": [], "total": 0, "avg_days_to_response": None}

        records = [
            {
                "status": a.status,
                "created_at": a.created_at,
                "updated_at": a.updated_at,
            }
            for a in apps
        ]
        df = pd.DataFrame(records)
        funnel = df.groupby("status").size().reset_index(name="count")
        df["days_waiting"] = (df["updated_at"] - df["created_at"]).dt.days
        avg_days = df["days_waiting"].mean()
        return {
            "funnel": funnel.to_dict(orient="records"),
            "total": len(apps),
            "avg_days_to_response": round(float(avg_days), 1) if not pd.isna(avg_days) else None,
        }

    def get_top_skills(self, limit: int = 10) -> list:
        with self.session_factory() as session:
            rows = (
                session.query(Skill.name, Skill.category)
                .join(VacancySkills, VacancySkills.skill_id == Skill.id)
                .all()
            )
        if not rows:
            return []
        df = pd.DataFrame(rows, columns=["name", "category"])
        top = (
            df.groupby(["name", "category"])
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(limit)
        )
        return top.to_dict(orient="records")

    def get_vacancy_dynamics(self, days: int = 30) -> list:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        with self.session_factory() as session:
            vacancies = (
                session.query(Vacancy)
                .filter(Vacancy.created_at >= cutoff)
                .all()
            )
        if not vacancies:
            return []
        df = pd.DataFrame([{"date": v.created_at.date()} for v in vacancies])
        dynamics = (
            df.groupby("date")
            .size()
            .reset_index(name="count")
            .sort_values("date")
        )
        dynamics["date"] = dynamics["date"].astype(str)
        return dynamics.to_dict(orient="records")

    def get_application_stats(self, user_id: int) -> dict:
        with self.session_factory() as session:
            apps = session.query(Application).filter(Application.user_id == user_id).all()
        if not apps:
            return {"conversion_rate": 0.0, "total": 0, "offers": 0, "rejections": 0}

        df = pd.DataFrame([{"status": a.status} for a in apps])
        total = len(df)
        offers = int((df["status"] == "offer").sum())
        rejections = int((df["status"] == "rejected").sum())
        conversion = round(offers / total * 100, 1) if total > 0 else 0.0
        return {
            "conversion_rate": conversion,
            "total": total,
            "offers": offers,
            "rejections": rejections,
        }
