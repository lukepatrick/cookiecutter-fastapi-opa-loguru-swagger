"""health module creates a health check for the API to determine if the API is properly responding/receiving
traffic

This health check is used when the API is deployed to Kubernetes to cut off traffic to APIs that are not
properly responding the the health check.

It is highly recommended the developer enhances the health check to check its
external connections to ensure the API is properly communicated to its necessary components. This is
especially important when its external connections are lazy connections.
"""

import fastapi
from fastapi import responses
from loguru import logger


router = fastapi.APIRouter()


@logger.catch
@router.get(
    "/",
    status_code=fastapi.status.HTTP_200_OK,
    responses={fastapi.status.HTTP_200_OK: {"model": str, "content": {"text/plain": {"example": "OK"}}}},
    response_class=responses.PlainTextResponse,
)
async def check_health() -> str:
    """Returns ok if there is a connection to the API endpoint"""
    return "Ok"
