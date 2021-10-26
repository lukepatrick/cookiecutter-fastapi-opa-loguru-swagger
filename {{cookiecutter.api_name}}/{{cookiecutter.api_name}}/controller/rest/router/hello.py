"""The hello router is an example of a get and post. It should be used as a starting point for developing the
API"""

import fastapi
from loguru import logger
from fastapi import responses
from fastapi import security

from {{cookiecutter.api_name}}.models.models import HelloWorld, HelloName
from {{cookiecutter.api_name}}.service import service
from {{cookiecutter.api_name}} import constructor

router = fastapi.APIRouter()
"""initializes an HTTP Bearer token security, use this bearer as a router dependency to mark those routes as
being secure. See API decorator below for an example of usage"""
bearer = security.HTTPBearer()


@logger.catch
@router.post(
    "/name",
    status_code=fastapi.status.HTTP_200_OK,
    description="The user posts the name to be greeted",
    response_description="Greets the name with a hello",
    dependencies=[
        fastapi.Depends(bearer)
    ],  # this line puts the "authorization" symbol on this endpoint. It also performs a validation that the
    # "Authorization" header is present in the request. The policy enforcement still needs to be performed
    # below. To remove auth, remove this DI and the policy enforcement below.
    responses={fastapi.status.HTTP_200_OK: {"model": HelloName}},
    response_class=responses.JSONResponse,
)
async def hello_name(
    request: fastapi.Request,
    name: HelloName,
    service: service.Service = fastapi.Depends(constructor.Service.get_service),
):
    """Responds by saying hello to the user.

    Take note of a few of the parameters.

    request: This is the raw HTTP request. This is used to get the authorization results from OPA
    service: This is a dependency injection to retrieve the service layer constructed in internal. Ensure the
                import and declaration match exactly like this example in future API endpoints
    name: The post body that is expected.
    """

    # This is the policy enforcement. The request.state.authorization comes from the auth middleware
    if not request.state.authorization.get("result", {}).get("allow", False):
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    return service.say_hello(name.hello)


@logger.catch
@router.get(
    "/world",
    status_code=fastapi.status.HTTP_200_OK,
    responses={fastapi.status.HTTP_200_OK: {"model": HelloWorld}},
    description="The user says hello, and the response will be to say hello",
    response_description="Returns a pleasant greeting",
    response_class=responses.JSONResponse,
)
async def hello_world(
    request: fastapi.Request,
    service: service.Service = fastapi.Depends(constructor.Service.get_service),
):
    """Returns ok if there is a connection to the API endpoint"""

    ret = HelloWorld(hello=service.get_world())
    return ret
