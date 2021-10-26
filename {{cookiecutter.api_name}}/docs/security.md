# API Security

As stated in the API standard, this template uses OPA to evaluate the policy of the input, and it is up to the user to enforce that policy.

## Running OPA locally
To run OPA locally, simply run `docker-compose up -d` and an OPA agent will startup. This agent defaults to port 8181 and mounts the policy located in the `policies` directory. 

## Writing rego
The policies are written in rego. Read the [documentation](https://www.openpolicyagent.org/docs/latest/policy-language/) when developing your policy

## How does it work
The OPA security is spread across 3+ files, the `auth.py`, `server.py`, the policy located in the policy folder, and the routes that enforce policies (in this example it is `hello.py`).

```
.
├── policies
│   └── {{cookiecutter.api_name}}.rego
└── {{cookiecutter.api_name}}/
    ├── controller/
    │   └── rest/
    │       ├── auth.py
    │       ├── router/
    │       │   └── hello.py
    │       └── server.py
    
```

Take a look at `server.py`
```python
# server.py

...

@app.middleware("http")
async def authorization(request: Request, call_next):
    """Authorization middleware sends all requests to OPA for evaluation
    authorization is middleware that intercepts every request and sends the request details to OPA. Where the
    policy is evaluated and the response is sent down to the endpoint for policy enforcement. This means that
    """
    resp = await auth.policy(request, config.settings.policy_url, config.settings.policy_path)
    request.state.authorization = resp
    resp = await call_next(request)
    return resp

```

This middleware is responsible for intercepting every request into the API and sending it to the `policy()` function in `auth.py`. In that function, the headers, cookies, path, and method are all extracted from the request and sent via HTTP to an OPA agent. 


In `auth.py`, the `policy()` function is responsible for sending information about the request to the OPA agent. The agent will then reply with a its evaluation of the policy. The response should look something like
```json
{
    "result": {
        "allow": false
    }
    // additional information may come back from OPA such as the JWT information
}
```
 If a failure case occurs, such as being unable to connect to the agent, then the response will just be `{}`.

Once the `policy()` function as returned the evaluation, the `auth.py` middleware will save the results in the requests' state in the `requests.state.authorization` property which can later be retrieved by the REST endpoints. Take the `controller/rest/router/hello.py` for example. 

```python
@router.post("/name")
async def hello_name(
    request: fastapi.Request,
    name: HelloName,
    service: service.Service = fastapi.Depends(constructor.Service.get_service),
):

    if not request.state.authorization.get("result", {}).get("allow", False):
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    return service.say_hello(name.hello)
```

Take the raw request by specifying the `fastapi.Request` in the method signature. Then the results can be retrieved from
`request.state.authorization`. In this example, the API returns unauthorized if allow was false.