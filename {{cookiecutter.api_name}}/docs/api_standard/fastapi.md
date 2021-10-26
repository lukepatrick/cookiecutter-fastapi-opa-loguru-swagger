# FastAPI
FastAPI is a high performance async web framework used for creating RESTful endpoints.

## Std Library
[fastapi](https://fastapi.tiangolo.com/)

## Async everywhere
In many of the operations, the most time consuming component to most APIs is IO. Calls to databases, network devices, IT systems block many of the synchronous APIs. This is minimized by scaling horizontally, allowing many workings and processing distribute the work. This still does leaves a lot of resources blocked by IO operations. 

FastAPI was chosen because of its use of use of ASGI (Asynchronous Server Gateway Interface) [starlette](https://github.com/encode/starlette) backend and [uvicorn](https://www.uvicorn.org/) ASGI server processor. Meaning the entire API is asynchronous from start to finish.

## Development and Operation

It is highly recommended to read the official documentation before trying to develop FastAPI controllers.

