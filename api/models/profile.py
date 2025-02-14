import json
from typing import Any
from uuid import uuid4

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import Select

from api.database import Base, db, select
from api.services.auth import get_name
from api.services.skills import get_skill_levels, get_skills


class Profile(Base):
    __tablename__ = "profiles_profile"

    id: Mapped[str] = Column(String(36), primary_key=True, unique=True)
    user_id: Mapped[str] = Column(String(36), nullable=False)

    public: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    async def serialize(self, include_user_id: bool = False, include_skills: bool =False) -> dict[str, Any]:
        skills = await get_skills() or {}
        leveled_skills = await get_skill_levels(self.user_id) or {}

        profile: dict[str, Any] = {
            "id": self.id,
            "public": self.public,
            "name": await get_name(self.user_id) or ""
        }

        if include_user_id:
            profile["user_id"] = self.user_id
        if include_skills:
            profile["skills"] = [
                {**vars(skills.get(skill)), "level": level} for skill, level in leveled_skills.items() if level > 0
            ]

        return profile

    @classmethod
    async def create(cls, user_id: str, public: bool = False) -> "Profile":
        profile = cls(id=str(uuid4()), user_id=user_id, public=public)
        await db.add(profile)
        return profile

    @staticmethod
    def filter_by_user_id(user_id: str) -> Select:
        return select(Profile).where(Profile.user_id == user_id)
