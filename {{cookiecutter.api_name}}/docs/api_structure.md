# API Structure

The cookiecutter structure follows the [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) pattern first set forth by Uncle Bob. If you are unfamiliar with this coding pattern, check out the [resources](##Additional-Resources)

This pattern is chosen because it separates the concerns of each layer into its composable elements. What this does is allow the create code that focuses on a single component of the application such as business logic, data retrieval, restful controllers, message bus controllers, and more. Then take each of these layers and compose them together into one service.

This separation has its advantages. Lets say the data source has changed for the API, the layered approach allows the developer to change the data layer to interact with the new source without having to change the business logic or the controllers (or at least impact is minimal). Another example is the requirements for the API changed and it is no longer a REST endpoint, rather it listens to a message bus. This architecture allows for the controller layer to be changed, but the lower layers to be unaffected.

Another advantage of clean architecture is testability. Separating the concerns allows for each layer to be able to be tested independent of one another. This is especially useful if test driven development is used in its creation.

## Directory Layout
This section covers the source code layout of the API template and will go through each file and directory, explaining their purpose .

A pizza delivery order API will be used as an example to understand the purpose of each of these layers. 

```
.
└── {{cookiecutter.api_name}}
    ├── controller/
    │   └── rest/
    │       └── router/
    ├── models/
    ├── repository/
    └── service/
```
### **Controller**
This directory is controller layer of clean architecture. The controller does not have to be restful. If the API calls for a message bus, then create a directory for it (ex. controller/message_bus). It could have multiple controllers. 

By default, the API template creates a FastAPI restful controller. It also creates the `controller/rest/router` directory because it uses the [APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter) method of creating APIs.

The controller layer is only responsible for receiving information in a manner that is compatible with the service layer. No business logic should be placed in this layer.

**pizza example**

When a customer orders a pizza to go, the controller layer is invoked in some way, either through a message bus, or an Website hitting the API endpoint. The controller layer receives the request from the customer. It can then validate the information received, ensure the user's credentials are correct, and respond to the system that invoked it if there is a problem. If the information is valid, it will then call the service layer to process the information based on the business requirements. The service layer could respond to the request (like the customer is ineligible) and the controller layer then responds back to the request.

### **Models**
Models are where all of the API models reside. This is sometimes referred to as the domain or the entity. The information the user is seeking or pushing through the API. Restful endpoint models, and external data models should reside here.

**pizza example**

The models of the customer information, pizza order, restful responses, etc. are all placed here.

### **Service**
The service layer, also called the use cases, provides the business logic necessary for the application. This layer can call down to the repository layer to retrieve information necessary to process the request from the controller layer. Think of this layer as being where most of the `if then` logic is placed. 

**pizza example**

If a customer places a delivery order for pizza, the service layer may ask the repository layer how far away the customer is from the restaurant. The service layer then takes that information and determines whether the customer is eligible for delivery. If they are ineligible, they will deny the request. Otherwise they will continue the order.

### Repository
The repository (sometimes called the access layer) is where external calls are made. This layer is responsible for any external systems that are interacted with. Examples of external systems includes other APIs, databases, a message bus, workflow engines, etc. This layer is needed to separate the business logic from the concerns of connecting to other systems. The repository returns needed information for the service to process requests.

**pizza example**

When the service layer wanted to know how far the user was, the repository layer was connected to the Google Maps API. It sent that customer information to Google Maps to determine the distance between the user and the restaurant they requested the pizza from. When Google Maps returned the data, it was then returned to the service layer.


## Construction of the layers

All of these layers need to be constructed together to form this API. The template tool provides a working example of this construction as well as a very basic service and repository layer to get the user started.

Take a look at the constructor.py file

```
.
└── {{cookiecutter.api_name}}
    └── constructor.py
```

There is a method in the `Service` class that looks like
```python
# constructor.py
...
    @classmethod
    async def construct(cls,):
        """construct is the initialization of the service and repository layer.

        This is just a the hello world example initialization. Override this method with the needed
        constructor
        """
        cls._repository = repository.Repository()
        cls._service = service.Service(cls._repository)
```

Here we can see the repository class is being instantiated. That repository class then is passed to the service class as a parameter. When developing the API, more than likely there will be additional parameters that needed to construct the repository and service layer, but the base construction will look the same. The service layer takes the repository instance and makes calls to it.

The final layer to construct is the controller layer. For this template, DI (dependency injection) is used for the controller to talk to the service layer. Look at the `server.py` file

```
.
└── {{cookiecutter.api_name}}
    ├── controller/
    │   └── rest/
            └── server.py

```

```python
# controller/rest/server.py

from my_api import constructor

@app.on_event("startup")
async def startup_server():
    """startup_server initializes the internal app before traffic can be received.
    startup_server is any items that need to initialize before the server can accept requests. This point is
    where we run the internal package startup in order to build the layers of the API.
    """
    await constructor.Service.construct()
    # add additional startup items here
```
This line here runs the constructor to create the service layer. Once this is constructed, each api endpoint could retrieve the instantiated service layer through DI. For example,
```python
# controller/rest/router/order.py

from my_api import constructor


@router.post("/order")
async def order_pizza(
    request: fastapi.Request,
    name: HelloName,
    # This fastapi.Depends injects the command "get_service" which returns the instance of the service and provides the method a way to call the service layer.
    service: service.Service = fastapi.Depends(constructor.Service.get_service),
):
```

> **Important Note:** the constructor ALWAYS has to be imported at the module level. Meaning if the user imports the module variable, the values will be None because of the way python handles imports.
> 
> **Bad:** `from my_api.constructor import Service`
>
> **Good:** `from my_api import constructor`

Now we have a controller layer that can call the service layer that can call the repository layer.

### **configuration of the layers**
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



## Additional Resources
https://pusher.com/tutorials/clean-architecture-introduction
