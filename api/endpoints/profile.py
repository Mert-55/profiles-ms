"""Endpoints related to the profile."""

from typing import Any

from fastapi import APIRouter

from api import models
from api.auth import get_user
from api.database import db
from api.exceptions.auth import admin_responses
from api.exceptions.profile import ProfileNotFoundError
from api.schemas.profile import Profile, PublicProfile, UpdateProfile
from api.utils.docs import responses


router = APIRouter()


@router.get("/profiles/profile/{profile_id}", responses=responses(PublicProfile, ProfileNotFoundError))
async def get_profile(profile_id: str) -> Any:
    """
    Return a public profile by its unique identifier.
    """

    if not (profile := await db.get(models.Profile, id=profile_id)) or profile.public is False:
        raise ProfileNotFoundError

    return await profile.serialize(include_skills=True)


@router.get("/profiles/user/{user_id}", responses=admin_responses(Profile))
async def update_profile(user_id: str = get_user(require_self_or_admin=True)) -> Any:
    """
    Return a public profile by user ID. Automatically creates a new profile if none exists.

    *Requirements:* **ADMIN** or **SELF**
    """
    profile = (
        exist_profile
        if (exist_profile := await db.first(models.Profile.filter_by_user_id(user_id)))
        else await models.Profile.create(user_id=user_id)
    )
    return await profile.serialize(include_user_id=True)


@router.patch("/profiles/user/{user_id}", responses=admin_responses(Profile))
async def update_profile(data: UpdateProfile, user_id: str = get_user(require_self_or_admin=True)) -> Any:
    """
    Update existing profile. Automatically creates a new profile if none exists.

    *Requirements:* **ADMIN** or **SELF**
    """

    profile: models.Profile | None = await db.first(models.Profile.filter_by_user_id(user_id))
    public = data.public if data.public is not None else False

    if profile is None:
        profile = await models.Profile.create(user_id=user_id, public=public)
    elif profile.public != public:
        profile.public = public

    return await profile.serialize(include_user_id=True)
