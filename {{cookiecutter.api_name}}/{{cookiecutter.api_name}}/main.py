""" main performs only 3 actions, initialize the configuration, initialize the logging level, then start the
application

Constructing the layers is done in the `internal` module and called in the startup() method of the
controller.rest.server module
"""

import os
import uvicorn
from loguru import logger

from {{cookiecutter.api_name}}.controller.rest import server
from {{cookiecutter.api_name}} import config


if __name__ == "__main__":

    # The config file only takes .env filetypes. If it is set, then the code will attempt
    # to set the variables using the specified file. If it is not, then the code will try to
    # pull the environment variables
    conf_file = os.getenv("CONFIG_FILE")
    if conf_file:
        config.init_config_file(conf_file)
    else:
        config.init_config_env()

    uv_server = uvicorn.Server(
        uvicorn.Config(
            server.app,
            host="0.0.0.0",
            port=config.settings.server_port,
            log_level=config.settings.log_level.lower(),
        )
    )
    # this call is very important to happen just before the run() call. It intercepts the logger created by
    # the uvicorn server and setups loguru
    config.setup_logging(config.settings.log_level, json_logs=False)
    logger.info(f"starting application on  {config.settings.server_host}:{config.settings.server_port}")
    logger.info(f"docs are available on ::{config.settings.server_port}{server.base_url}/docs")
    uv_server.run()
