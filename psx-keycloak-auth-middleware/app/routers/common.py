from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=[""])
def service():
    return {"name": "keycloak-auth-middleware"}


@router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
