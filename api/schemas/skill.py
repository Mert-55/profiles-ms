from pydantic import BaseModel, Extra


class Skill(BaseModel):
    id: str
    parent_id: str
    name: str
    dependencies: list[str]
    dependents: list[str]

    class Config:
        extra = Extra.ignore


class LeveledSkill(Skill):
    level: int
