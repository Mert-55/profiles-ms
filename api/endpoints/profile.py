"""Endpoints related to the profile."""

from typing import Any

from fastapi import APIRouter

from api import models
from api.auth import get_user
from api.database import db
from api.exceptions.auth import admin_responses, user_responses
from api.exceptions.profile import ProfileNotFoundError
from api.schemas.profile import Profile, PublicProfile, UpdateProfile
from api.utils.docs import responses


router = APIRouter()


@router.get("/profile/{profile_id}", responses=responses(PublicProfile, ProfileNotFoundError))
async def get_public_profile(profile_id: str) -> Any:
    """
    Return a public profile by its unique identifier.
    """

    if not (profile := await db.get(models.Profile, id=profile_id)) or profile.public is False:
        raise ProfileNotFoundError

    return await profile.serialize(include_skills=True, include_user=True)


@router.get("/user/{user_id}/public-status", responses=user_responses(Profile))
async def get_public_status(user_id: str = get_user(require_self_or_admin=True)) -> Any:
    """
    Return a public profile by user ID. Automatically creates a new profile if none exists.

    *Requirements:* **ADMIN** or **SELF**
    """
    profile = (
        exist_profile
        if (exist_profile := await db.first(models.Profile.filter_by_user_id(user_id)))
        else await models.Profile.create(user_id=user_id)
    )
    return await profile.serialize()


@router.put("/user/{user_id}/public-status", responses=user_responses(Profile))
async def replace_public_status(data: UpdateProfile, user_id: str = get_user(require_self_or_admin=True)) -> Any:
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

    return await profile.serialize()
