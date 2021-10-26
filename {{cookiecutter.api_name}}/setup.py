from setuptools import setup

with open("requirements.txt") as f:
    required = []
    for line in f:
        if not line.startswith(
            (
                "-",
                "#",
            )
            or line.sispace()
        ):
            required.append(line.partition(" ")[0].rstrip("\n"))

try:
    import pypandoc

    description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    try:
        description = open("README.txt").read()
    except (IOError, ImportError):
        description = open("README.md").read()

setup(
    name="{{cookiecutter.api_name}}",
    version="0.0.1",
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.author_email}}",
    packages=[
        "{{cookiecutter.api_name}}",
        "{{cookiecutter.api_name}}.controller",
        "{{cookiecutter.api_name}}.controller.rest",
        "{{cookiecutter.api_name}}.controller.rest.router",
        "{{cookiecutter.api_name}}.models",
        "{{cookiecutter.api_name}}.repository",
        "{{cookiecutter.api_name}}.service",
    ],
    license="MIT License",
    include_package_data=True,
    long_description=description,
    install_requires=required,
)
