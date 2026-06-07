from pydantic import BaseModel
from typing import Literal



class ExtractedSkill(BaseModel):
    name: str
    type: Literal["hard", "soft", "tool"]


class SkillExtractionResult(BaseModel):
    skills: list[ExtractedSkill]
