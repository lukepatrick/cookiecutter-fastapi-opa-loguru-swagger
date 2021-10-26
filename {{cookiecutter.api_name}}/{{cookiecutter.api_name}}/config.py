"""config module is all of the environment variables or file variables necessary for the API

All configs should be placed into the Settings class. When the api starts up in *main.py*, the init()
will be called and the settings should be available to all modules. For example:
    ```
    from <api name> import config

    log_lvl = config.settings.log_level
    ```

It is important to import this at a module level (ex. from <api name> import config),
NOT a class (ex. from <api name>.config import settings). This is due to how python constructs its imports.

Settings are initialized in the *main.py* and usable throughout the application afterwards.
"""

from typing import Optional
import sys
import logging

from loguru import logger
import pydantic


# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(pydantic.BaseSettings):
    # these are base settings, it is not recommended to remove any of these configurations
    server_port: int = 8080
    server_host: str = "0.0.0.0"
    log_level: str = "INFO"
    log_json: bool = False
    policy_url: str = "http://localhost:8181"
    policy_path: str = "/v1/data/{{cookiecutter.api_name}}/authz"


settings: Optional[Settings] = None


def init_config_env():
    global settings
    settings = Settings()


def init_config_file(filename: str):
    global settings
    settings = Settings(_env_file=filename, _env_file_encoding="utf-8")


# intercepts the fastapi and uvicorn logging handler and replaces it with loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(log_level: str, json_logs: bool = False):
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": json_logs}])
