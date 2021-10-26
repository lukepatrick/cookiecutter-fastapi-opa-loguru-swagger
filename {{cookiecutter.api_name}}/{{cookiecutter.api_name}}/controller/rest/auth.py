""" auth module is responsible for sending the user's request to the Open Policy Agent for policy evaluation.
Once the policy has been evaluated, the response of the OPA agent is sent back down to the REST endpoint for
policy enforcement.

Read the OPA docs to understand how policy evaluation is done
https://www.openpolicyagent.org/docs/latest/


To understand what this module is accomplishing, it is necessary to understand the two terms above

policy evaluation - observe and compare the policy against the input date to determine if the input is allowed
or not. policy enforcement - observing the evaluation in compliance with authorization (ie. raise 401/403 if
the policy determines it is not allowed.
"""

from typing import Dict

import aiohttp
import fastapi
from loguru import logger
import json


def convert_header(header):
    """Converts fastapi headers into a dict of strings
    FastAPI comes in as a tuple of byte strings. convert_header turns those headers into a dict of str.
    This is necessary for the JSON marshalling to work.
    """
    res = dict()
    for a, b in header:
        res[a.decode("utf-8")] = b.decode("utf-8")
    return res


async def policy(request: fastapi.Request, policy_url: str, policy_path: str) -> Dict:
    """send the fastapi request's path, method, headers, and cookies to OPA for evaluation"""
    policy_url = f"{policy_url}{policy_path}"

    body = {
        "input": {
            "path": request.url.path,
            "method": request.method,
            "headers": convert_header(request.headers.raw),
            "cookies": request.cookies,
        }
    }

    # consuming the request body is generally discouraged,
    # issue: https://github.com/encode/starlette/issues/495#issuecomment-494008175
    #
    # req_body = await request.body()
    # req_body = req_body.decode("utf-8")
    # try:
    #     json_body = json.loads(req_body)
    #     req_body = json_body
    # except Exception:
    #     pass
    # body["input"]["body"] = req_body

    logger.debug(f"sending policy to {policy_url}")
    policy_input = json.dumps(body, indent=2)
    logger.debug(f"policy input: {policy_input}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(policy_url, data=policy_input) as rsp:
                policy_resp = await rsp.json()
                if rsp.status >= 300:
                    logger.info(
                        "Error checking auth, got status %s and message: %s" % (rsp.status, await rsp.text())
                    )
                    return {}
                logger.debug(f"Auth response {json.dumps(policy_resp, indent=2)}")
                return policy_resp
        except Exception as err:
            logger.error(err)
            return {}
