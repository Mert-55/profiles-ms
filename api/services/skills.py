from typing import cast

from api.schemas.skill import Skill
from api.services.internal import InternalService
from api.utils.cache import redis_cached


@redis_cached("skills")
async def get_skills() -> dict[str, Skill]:
    async with InternalService.SKILLS.client as client:
        response = await client.get("/skills")
        return {skill.id: skill for skill in map(Skill.parse_obj, response.json())}


@redis_cached("user_skills", "user_id")
async def get_skill_levels(user_id: str) -> dict[str, int]:
    async with InternalService.SKILLS.client as client:
        response = await client.get(f"/skills/{user_id}")
        return cast(dict[str, int], response.json())
