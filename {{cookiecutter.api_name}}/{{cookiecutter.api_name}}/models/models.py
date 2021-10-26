import pydantic


class HelloWorld(pydantic.BaseModel):
    hello: str = pydantic.Field(
        alias="hello",
        default="world",
        description="Says hello to the world",
        example="world",
    )


class HelloName(pydantic.BaseModel):
    hello: str = pydantic.Field(
        alias="hello",
        description="Says hello to a user",
        example="bob",
    )
