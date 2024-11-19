import json
import logging
from fastapi import HTTPException
from keycloak.keycloak_openid import KeycloakOpenID
from keycloak.openid_connection import KeycloakOpenIDConnection
from keycloak.keycloak_uma import KeycloakUMA
from keycloak.exceptions import KeycloakPostError

from ..config import load

logger = logging.getLogger(__name__)
config = load.Settings()

keycloak_config = config.keycloak

keycloak_openid = KeycloakOpenID(
    server_url=keycloak_config.url,
    realm_name=keycloak_config.realm,
    client_id=keycloak_config.client_id,
    client_secret_key=keycloak_config.client_secret,
)

keycloak_openid_conn = KeycloakOpenIDConnection(
    server_url=keycloak_config.url,
    realm_name=keycloak_config.realm,
    client_id=keycloak_config.client_id,
    client_secret_key=keycloak_config.client_secret,
)

keycloak_uma = KeycloakUMA(connection=keycloak_openid_conn)

def get_resource_metadata(resource_id: str):
    try:
        print(keycloak_uma.uma_well_known)
        resource_metadata = keycloak_uma.resource_set_read(resource_id)
        return resource_metadata
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Unexpected error")


def get_permission(access_token: str, resource: str, scope: str):
    try:
        permissions = keycloak_openid.uma_permissions(
            token=access_token,
            permissions=f"{resource}#{scope}"
        )
        resource_id = permissions[0]["rsid"]
        return resource_id

    except KeycloakPostError as e:
        logger.error(e)
        error_json = json.loads(e.response_body.decode('utf-8'))
        raise HTTPException(
            status_code=e.response_code, detail=error_json)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Unexpected error")


def get_resources():
    try:
        resources = keycloak_uma.resource_set_list()
        return resources
    except KeycloakPostError as e:
        logger.error(e)
        error_json = json.loads(e.response_body.decode('utf-8'))
        raise HTTPException(
            status_code=e.response_code, detail=error_json)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Unexpected error")


def get_resource_id_by_name(resource_name: str):
    try:
        resource_metadata = keycloak_uma.resource_set_list_ids(
            name=resource_name)
        return resource_metadata
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail="Unexpected error")

