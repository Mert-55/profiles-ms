from api.schemas.user import UserInfo
from api.services.internal import InternalService
from api.utils.cache import redis_cached


@redis_cached("user", "user_id")
async def exists_user(user_id: str) -> bool:
    async with InternalService.AUTH.client as client:
        response = await client.get(f"/users/{user_id}")
        return response.status_code == 200


@redis_cached("user", "user_id")
async def get_user_info(user_id: str) -> UserInfo | None:
    async with InternalService.AUTH.client as client:
        response = await client.get(f"/users/{user_id}")
        if response.status_code != 200:
            return None
        dt = response.json()
        return UserInfo(
            name=dt["name"],
            tags=dt["tags"],
            description=dt["description"],
            registration=dt["registration"],
            avatar_url=dt["avatar_url"],
        )
