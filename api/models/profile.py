import json
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import Select
from sqlalchemy.testing import exclude

from api.database import Base, db, select
from api.services.auth import get_user_info
from api.services.skills import get_skill_levels, get_skills, get_profile_skills


class Profile(Base):
    __tablename__ = "profiles_profile"

    id: Mapped[str] = Column(String(36), primary_key=True, unique=True)
    user_id: Mapped[str] = Column(String(36), nullable=False)

    public: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    async def serialize(self, include_user: bool = False, include_skills: bool = False) -> dict[str, Any]:
        _leveled_skills = len(await get_skill_levels(self.user_id) or {})
        user = await get_user_info(self.user_id) or {}

        profile: dict[str, Any] = {
            "id": self.id,
            "public": self.public,
            "name": user.name or "",
            "total_skills": _leveled_skills,
        }

        if include_user:
            profile["user"] = user.dict(
                exclude={"name"}) if user.name else user
        if include_skills:
            profile["root_skills"] = await get_profile_skills(self.user_id)

        return profile

    @classmethod
    async def create(cls, user_id: str, public: bool = False) -> "Profile":
        profile = cls(id=str(uuid4()), user_id=user_id, public=public)
        await db.add(profile)
        return profile

    @staticmethod
    def filter_by_user_id(user_id: str) -> Select:
        return select(Profile).where(Profile.user_id == user_id)
