"""The repository is external connections, ie. a data connection layer

This is an example repository that doesn't actually make an external connection and is used only for education
purposes. Override this repository with external connections needed.
"""


class Repository:
    def __init__(self):
        pass

    def get_world(self):
        return "world"
