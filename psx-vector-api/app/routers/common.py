from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=[])
def service():
    return {"name": "vector-api"}


@router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
