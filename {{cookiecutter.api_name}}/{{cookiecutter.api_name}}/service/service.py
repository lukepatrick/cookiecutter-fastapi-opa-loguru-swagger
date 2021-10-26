""" service module is where the business logic is applied. It does not care about how users connect to the
function, that responsibility is the controller. It does not care how it receives data, that responsibility
lies with the repository layer. It is the business logic of the API, the service that it provides.

Below is just an example of a service

"""

from typing import Dict

from {{cookiecutter.api_name}}.repository import repository


class Service:
    def __init__(self, repo: repository.Repository):
        self.repo = repo
        pass

    def get_world(self):
        # here is where I would apply business logic to getting world, in this case there is nothing special
        # to do
        return self.repo.get_world()

    def say_hello(self, name: str) -> Dict[str, str]:
        # here is an example of business logic applied to the name

        if name.lower() == "luke" or name.lower() == "ian":
            return {"go away": "not welcome"}

        return {
            "hello": name,
        }
