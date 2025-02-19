from pydantic import BaseModel, Field

from .skill import LeveledSkill
from .user import UserInfo


class PublicProfile(BaseModel):
    id: str = Field(description="The Profile's unique identifier")
    public: bool = Field(description="Whether the profile is public")
    name: str = Field(description="The username")
    user: UserInfo = Field(description="The public user information.")
    total_skills: int = Field(description="The total number of skills gained.")
    skills: list[LeveledSkill] | None = Field(description="The Skills gained by the user")


class Profile(PublicProfile):
    id: str = Field(description="The Profile's unique identifier")
    public: bool = Field(description="Whether the profile is public")
    name: str = Field(description="The username")
    total_skills: int = Field(description="The total number of skills gained.")


class UpdateProfile(BaseModel):
    public: bool | None = Field(False, description="Whether the profile is public")
