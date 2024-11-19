import logging
import requests
import json

from enum import Enum
from typing import Dict, Optional
from pydantic import ValidationError
from fastapi import APIRouter, HTTPException, Path, Depends, Request
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.models.payloads import RequestBody, ResponseBody
from app.repo.keycloak import keycloak_openid, config, get_resource_metadata, get_permission
from app.utils.status_queue import get_status_queue


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"


router = APIRouter()

logger = logging.getLogger(__name__)

keycloak_url = config.keycloak.url
service_url = f"0.0.0.0:{config.port}"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=keycloak_openid.auth_url(
        redirect_uri=f"{service_url}/callback"),
    tokenUrl=f"{keycloak_url}/token"
)


def fetch_resource_data(
        method: HTTPMethod,
        url: str,
        query_params: Dict[str, Optional[str]],
        body: Optional[Dict[str, str]] = {}
):
    try:
        logger.info(f"Fetching data from {url}?{query_params}\ndata={body}")
        if (method == HTTPMethod.GET):
            response = requests.get(url, params=query_params)
        elif (method == HTTPMethod.POST):
            response = requests.post(url, params=query_params, json=body)
        else:
            raise HTTPException(
                status_code=400, detail="Invalid HTTP method")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Failed to access resource")

        return response.json()
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Unexpected error")


@router.get("/{resource}/invoke", tags=["resource"])
async def get_resource(
    request: Request,
    resource: str = Path(..., description="Resource name"),
    access_token: str = Depends(oauth2_scheme),
):
    scope = "read"
    user_info = keycloak_openid.decode_token(access_token, validate=False)

    logger.info(
        f"Checking permissions on {resource} for {user_info['name']}..."
    )
    resource_id = get_permission(access_token, resource, scope)

    logger.info(
        f"Getting resource metadata {resource} for {user_info['name']}..."
    )
    resource_metadata = get_resource_metadata(resource_id)

    logger.info(f"Getting resource data {resource} for {user_info['name']}...")
    resource_data = fetch_resource_data(
        method=HTTPMethod.GET,
        url=resource_metadata["uris"][0],
        query_params=request.query_params)
    return resource_data


@router.post("/{resource}/invoke", tags=["resource"])
async def post_resource(
    request: Request,
    resource: str = Path(..., description="Resource name"),
    access_token: str = Depends(oauth2_scheme),
):
    status_queue = get_status_queue()

    # Clear the status queue on new request
    with status_queue.mutex:
        status_queue.queue.clear()
        status_queue.all_tasks_done.notify_all()
        status_queue.unfinished_tasks = 0

    user_info = keycloak_openid.decode_token(access_token)
    request_body: RequestBody = await request.json()

    # Validate request body
    try:
        RequestBody(**request_body)
    except ValidationError as e:
        logger.error(e.json())
        raise HTTPException(status_code=400, detail="Invalid request body")

    # Initialize response body
    users: list[str] = request_body["user_data_requested"]
    response: ResponseBody = {
        "data": {user: {} for user in request_body['user_data_requested']},
        "errors": []
    }

    auth_user = user_info["email"]
    sse_auth_messages = []

    # Check permissions & request data for each user defined in `user_data_requested`
    for user in users:
        sse_message = {}

        scope = f"{request_body['type']}-{user}"
        users_to_request: list[str] = users.copy()

        # scope format: `{type}-{usermail}`
        resource_type, data_owner = scope.split('-')

        # hardcoded retrieval of name, since we know the structure, for the demo
        user_first_name = auth_user.split('@')[0].capitalize()
        sse_message["user"] = user_first_name

        # Suffix for logging: what to put behind the type
        suffix = ""
        if request_body['type'] == "calendar":
            suffix = "data"
        elif request_body['type'] == "medical" or request_body['type'] == "financial" or request_body['type'] == "all":
            suffix = "records"
        sse_message["type"] = resource_type.capitalize()

        logger.info(
            f"Checking permissions {user}'s resource {resource}#{scope} for {user_info['email']}...")
        sse_message["data_owner"] = data_owner.capitalize()
        try:
            resource_id = get_permission(
                access_token, resource, scope)
            sse_message["status"] = "Access granted"
        except:
            users_to_request.remove(user)
            request_body["user_data_requested"] = users_to_request
            response["errors"].append(
                f"Access denied. {user_info['given_name']} does not have the neccessary permissions to access {user_first_name}'s {request_body['type']} {suffix}")
            sse_message["status"] = "Access denied"

            sse_auth_messages.append(sse_message)
            continue

        logger.info(
            f"Getting resource metadata {user}'s resource {resource}#{scope} for {user_info['email']}...")
        try:
            resource_metadata = get_resource_metadata(resource_id)
        except:
            users.remove(user)
            response["errors"].append(
                f"Failed to access {user_first_name}'s {request_body['type']} {suffix}")

            sse_auth_messages.append(sse_message)
            continue

        logger.info(
            f"Getting resource data of {resource}#{scope} for {user_info['email']}...")

        try:
            resource_data = fetch_resource_data(
                method=HTTPMethod.POST,
                url=resource_metadata["uris"][0],
                query_params=request.query_params,
                body=request_body)
        except:
            response["errors"].append(
                f"Failed to access {user_first_name}'s {request_body['type']} {suffix}")
            sse_auth_messages.append(sse_message)
            continue

        response["data"][user] = resource_data

        sse_auth_messages.append(sse_message)

    status_queue.put(json.dumps(sse_auth_messages))

    return response
