from typing import Any, cast

from api.services.internal import InternalService
from api.utils.cache import redis_cached


@redis_cached("user", "user_id")
async def exists_user(user_id: str) -> Any:
    async with InternalService.AUTH.client as client:
        response = await client.get(f"/users/{user_id}")
        return response.status_code == 200


@redis_cached("user", "user_id")
async def get_name(user_id: str) -> str | None:
    async with InternalService.AUTH.client as client:
        response = await client.get(f"/users/{user_id}")
        if response.status_code != 200:
            return None
        return cast(str | None, response.json()["name"])
