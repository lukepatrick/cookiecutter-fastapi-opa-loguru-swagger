"""server module is the constructor for FASTPI apps. This module is where middleware, routers, startup and the
base app is created. This module should only be touch when either:
    1. adding a new router
    2. adding/modifying middleware
    3. changing the startup
"""


import fastapi
from fastapi import Request
from fastapi.middleware import cors, gzip
from instana.middleware import InstanaASGIMiddleware

from {{cookiecutter.api_name}} import config
from {{cookiecutter.api_name}}.controller.rest.router import health
from {{cookiecutter.api_name}}.controller.rest.router import hello
from {{cookiecutter.api_name}}.controller.rest import auth
from {{cookiecutter.api_name}} import constructor


base_url = "{{cookiecutter.api_base_url}}"


app = fastapi.FastAPI(
    openapi_url=f"{base_url}/openapi.json",
    docs_url=f"{base_url}/docs",
    redoc_url=f"{base_url}/redoc",
    title="{{cookiecutter.api_name}}",
    description="{{cookiecutter.api_description}}",
    version="0.0.1",
)


"""sets the CORS (https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) permission for the application. For
future consideration, it is unsecure to allow "*" origins and methods in production"""
app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""adds instana middleware for metrics and monitoring
https://www.instana.com/docs/ecosystem/python/components/asgi/"""
app.add_middleware(InstanaASGIMiddleware)


"""adds GZIP compression to all responses if the size of the response is over 1000 bytes and the user accepts
the encoding. Don't go below 1000 bytes as that is the inflection point where compression"""
app.add_middleware(gzip.GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def authorization(request: Request, call_next):
    """Authorization middleware sends all requests to OPA for evaluation
    authorization is middleware that intercepts every request and sends the request details to OPA. Where the
    policy is evaluated and the response is sent down to the endpoint for policy enforcement. This means that
    """
    resp = await auth.policy(request, config.settings.policy_url, config.settings.policy_path)
    request.state.authorization = resp
    resp = await call_next(request)
    return resp


@app.on_event("startup")
async def startup_server():
    """startup_server initializes the internal app before traffic can be received.
    startup_server is any items that need to initialize before the server can accept requests. This point is
    where we run the internal package startup in order to build the layers of the API.
    """
    await constructor.Service.construct()
    # add additional startup items here


"""uses the router method of fastAPI, see https://fastapi.tiangolo.com/tutorial/bigger-applications/
The health route is recommended to keep as it is needed for K8s health checks"""
app.include_router(health.router, prefix=f"{base_url}/health", tags=["health"])


"""This is an example route, not necessary to keep, but does show a good hello world example"""
app.include_router(hello.router, prefix=f"{base_url}/hello", tags=["hello"])
