# Running the API

## (Optional) Startup the OPA server

If the configuration is going to use a local OPA agent, start the default agent in the folder by running

`$ docker-compose up -d`

This will start an OPA agent in the background. 

> **Note:** This will use whatever policies are in place in the `policies/` directory

## Start the API
First, ensure the virtualenv was created by running

`$ make py-all`

Then run the API by simply execute the main function 
```
└── {{cookiecutter.api_name}}/
    └── main.py
```
which will look like

`$ ./venv/bin/python <your api name>.main.py`

or 

`$ make py-run`


## Using a .env file

If a .env file is used to set the configuration, export the name of the file

`$ export CONFIG_FILE=<path to the .env file>`

then run one of the above methods