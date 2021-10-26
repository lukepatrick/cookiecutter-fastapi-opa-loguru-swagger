# Configuration
In every API, it is important to variablize certain configurations that will later be provided either by the user or the environment it is spun up in. It is equally important to keep those variables in a single spot (or at least in as few spots as possible) to ensure maintainers can quickly find the configurations that are important to the application. To this extent, almost all configurations are placed in the `config.py` and uses the (pydantic settings to manage them.

## Std library
[pydantic-settings](https://pydantic-docs.helpmanual.io/usage/settings/)

## Why use pydantic settings and not os.getenv
The key difference between pydantic settings and os.getenv is the built in validation in pydantic. Take for example retrieving the log level. The developer would want to ensure that the log level is provided to the application. To achieve this in **pydantic settings** it would look something like
```python
# pydantic settings

import pydantic

class Settings(pydantic.BaseSettings):
    log_level: str

settings = Settings()
```

In this example, if the user does not provide the `LOG_LEVEL` environment variable, an exception is raised. This is all built into the pydantic BaseSettings class when it is instantiated. Alternatively, the settings could be provided through a .env configuration file.

```python
# pydantic settings
settings = Settings(_env_file="../local.env")
```

This is especially useful for large configurations. Other features includes typecasting the variables, setting defaults, custom validators, and more.

Compare this to the os.getenv
```python
# os.getenv

import os

class Settings:
    log_level: str

settings = Settings()
settings.log_level = os.getenv("LOG_LEVEL")
if not settings.log_level:
    raise RuntimeException("LOG_LEVEL env variable is not set")
```

While this does not look like much work, it quickly adds up with each config variable. It also does not provide typecasting, easy custom validators, etc. The succinctness of pydantic-settings is why this is chosen over os.getenv.