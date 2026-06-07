from pydantic import BaseModel
from typing import List, Optional


class FunnelItem(BaseModel):
    status: str
    count: int


class UserFunnelResponse(BaseModel):
    funnel: List[FunnelItem]
    total: int
    avg_days_to_response: Optional[float] = None


class SkillDemandItem(BaseModel):
    name: str
    category: Optional[str] = None
    count: int


class VacancyDynamicsItem(BaseModel):
    date: str
    count: int


class ApplicationStatsResponse(BaseModel):
    conversion_rate: float
    total: int
    offers: int
    rejections: int


class MatchResponse(BaseModel):
    vacancy_id: int
    match_percent: float
    user_skill_count: int
    vacancy_skill_count: int
    matched_count: int
