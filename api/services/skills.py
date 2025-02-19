from typing import cast
from collections import defaultdict

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

def _group_skills_by_root(
    existing_skills: dict[str, Skill], leveled_skills: dict[str, int]
) -> list[dict[str, any]]:
    root_skills_map = defaultdict(list)

    for skill_id, level in leveled_skills.items():
        if level < 1:
            continue

        if not (skill:= existing_skills.get(skill_id)):
            continue

        root_skill_id = skill.parent_id
        root_skills_map[root_skill_id].append({"skill": skill_id, "level": level})

    return [{"skill": root_id, "skills": skills} for root_id, skills in root_skills_map.items()]


async def get_profile_skills(user_id: str) -> list[dict[str, any]]:
    existing_skills = await get_skills()
    leveled_skills = await get_skill_levels(user_id)
    return _group_skills_by_root(existing_skills, leveled_skills)