from fastapi import status

from .api_exception import APIException


class ProfileNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Profile not found"
    description = "This profile does not exist."
