from typing import Optional

from pydantic import BaseModel, Extra, Field

from api.redis import auth_redis


class User(BaseModel):
    id: str
    email_verified: bool
    admin: bool


class UserInfo(BaseModel):
    name: Optional[str] = Field(default=None, description="Unique user name (used for login, case insensitive)")
    registration: int = Field(description="Timestamp of creation")
    description: Optional[str] = Field(default=None, description="Bio of the user profile")
    avatar_url: Optional[str] = Field(default=None, description="URL of the user's avatar")
    tags: list[str] = Field(description="Tags of the user profile")


class UserAccessTokenData(BaseModel):
    email_verified: bool
    admin: bool

    class Config:
        extra = Extra.ignore


class UserAccessToken(BaseModel):
    uid: str
    rt: str
    data: UserAccessTokenData

    class Config:
        extra = Extra.ignore

    def to_user(self) -> User:
        return User(id=self.uid, **self.data.dict())

    async def is_revoked(self) -> bool:
        return bool(await auth_redis.exists(f"session_logout:{self.rt}"))
