from typing import Optional
from pydantic import BaseModel, Extra


class Skill(BaseModel):
    id: str
    parent_id: str

    class Config:
        extra = Extra.ignore


class LeveledSkill(Skill):
    level: int
