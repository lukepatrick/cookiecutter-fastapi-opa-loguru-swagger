"""internal module is the constructor for the clean architecture layer. This should be use to construct the
repository layer and then the service layer. """

from typing import Optional

from {{cookiecutter.api_name}}.service import service
from {{cookiecutter.api_name}}.repository import repository


class Service:
    """The Service class constructs the Repository and Service layers using a singleton pattern. This pattern
     ensures connections are shared across multiple calls from the controller established once.

    Change the startup method to initialize the service and repository layer based on the API's needs.

    An example of initializing the code and using the service layer is as follows:
        '''
        from <api_module> import constructor

        # initialized the service
        await constructor.Service.startup()

        # grab the pointer to the service
        service = constructor.Service.get_service()

        # now the methods of the service layer are available
        service.foo()
        '''

    If the Service class is initialized in another module, it can be used in submodules like so:
        ```
        from <api_module> import constructor

        # since we are importing it as a module, and another module has already called the startup()
        # function, the user can retrieve the service
        service = constructor.Service.get_service()

        service.foo()
        ```

    it is important to import the internal package at a MODULE level (import internal). Do NOT import his
    module as a class (from internal import Service). This is because of the way python constructs
    imports. Importing it as a module will allow one module to initialize it and multiple modules to utilized
    the initialized service.

    """

    _service: Optional[service.Service] = None
    _repository: Optional[repository.Repository] = None

    def __init__(self):
        raise RuntimeError("Call construct() instead")

    @classmethod
    async def construct(cls):
        """construct is the initialization of the service and repository layer.

        This is just a the hello world example initialization. Override this method with the needed
        constructor
        """
        cls._repository = repository.Repository()
        cls._service = service.Service(cls._repository)

    @classmethod
    def get_service(cls):
        if not cls._service:
            raise RuntimeError("service not initiated, call startup() first")
        return cls._service

    @classmethod
    def get_repository(cls):
        if not cls._repository:
            raise RuntimeError("repository not initiated, call startup() first")
        return cls._repository
