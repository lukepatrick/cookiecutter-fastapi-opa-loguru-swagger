package {{cookiecutter.api_name}}.authz

default allow = false

# allow owner
allow {
	is_jwt_valid
}

allow {
	endswith(input.path, "/health")
}

allow {
	endswith(input.path, "/health/")
}

is_jwt_valid {
    secret = opa.runtime()["env"]["JWT"]
    jwt_str := input.headers.authorization
    jwt_rpl := replace(jwt_str, "Bearer ", "")
    io.jwt.verify_hs256(jwt_rpl, secret)
    [header, payload, signature] = io.jwt.decode(jwt_rpl)
}

jwt = {"payload": payload} {
    jwt_str := input.headers.authorization
    jwt_rpl := replace(jwt_str, "Bearer ", "")
	[header, payload, signature] = io.jwt.decode(jwt_rpl)
}
