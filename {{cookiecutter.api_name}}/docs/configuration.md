# Configuration
Configuration is necessary, especially when the startup environment for the API is different. The configuration is set when the API is started and then is retrievable throughout the whole application.

Lets look at how the configuration is constructed.
```
.
└── {{cookiecutter.api_name}}
    ├── config.py
    └── main.py
    
```
```python
import pydantic


# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(pydantic.BaseSettings):
    # these are base settings, it is not recommended to remove any of these configurations
    google_api_url: str


settings: Optional[Settings] = None


def init_config_env():
    global settings
    settings = Settings()


def init_config_file(filename: str):
    global settings
    settings = Settings(_env_file=filename, _env_file_encoding="utf-8")
...
```
```python
# main.py
if __name__ == "__main__":

    # The config file only takes .env filetypes. If it is set, then the code will attempt
    # to set the variables using the specified file. If it is not, then the code will try to
    # pull the environment variables
    conf_file = os.getenv("CONFIG_FILE")
    if conf_file:
        config.init_config_file(conf_file)
    else:
        config.init_config_env()
    ...
```

What happens is when the `main.py` is called. It will call the `config.init_config_file` or the `config.init_config_env` to retrieve variables from either a file or the environment. After which the global variable `settings` will be instantiated and available for the application.

We can then take that configuration and use it in our constructor to build the layers

```python
# constructor.py

from my_api import config

...

    @classmethod
    async def construct(cls,):
        """construct is the initialization of the service and repository layer.

        This is just a the hello world example initialization. Override this method with the needed
        constructor
        """
        cls._repository = repository.Repository(config.settings.google_api_url)
        cls._service = service.Service(cls._repository)

```

> **Important Note:** the config ALWAYS has to be imported at the module level. Meaning if the user imports the module variable, the values will be None because of the way python handles imports.
> 
> **Bad:** `from my_api.config import settings`
>
> **Good:** `from my_api import config`

