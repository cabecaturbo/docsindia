from fastapi import APIRouter


router = APIRouter()


@router.post("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


