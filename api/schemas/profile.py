from pydantic import BaseModel, Field

from .skill import LeveledSkill


class PublicProfile(BaseModel):
    id: str = Field(description="The Profile's unique identifier")
    public: bool = Field(description="Whether the profile is public")
    name: str = Field(description="The username")
    skills: list[LeveledSkill] | None = Field(description="The Skills gained by the user")


class Profile(PublicProfile):
    user_id: str = Field(description="The user's unique identifier")


class UpdateProfile(BaseModel):
    public: bool | None = Field(False, description="Whether the profile is public")
