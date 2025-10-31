from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from fastapi import HTTPException
from ..cache import cache_get, cache_set, content_hash, rate_limit_allow


router = APIRouter()


class DocMeta(BaseModel):
    typeHint: str | None = None
    pages: int | None = None


class ExplainRequest(BaseModel):
    docText: str
    docMeta: DocMeta
    locale: str
    hints: bool | None = False
    deviceId: str


@router.post("/explain")
def explain(req: ExplainRequest) -> dict[str, Any]:
    if not rate_limit_allow(req.deviceId):
        raise HTTPException(status_code=429, detail="Too many requests")
    text = req.docText.strip()
    key = f"explain:{content_hash(text)}"
    cached = cache_get(key)
    if cached:
        return cached
    # naive heuristic classifier
    doc_type = req.docMeta.typeHint or ("credit-card-statement" if "statement" in text.lower() else "generic")

    # dummy extraction
    extractions: dict[str, Any] = {}
    if doc_type == "credit-card-statement":
        extractions = {
            "issuer": "Unknown",
            "totalDue": None,
            "dueDate": None,
            "fees": []
        }

    summary = "Summary unavailable" if not text else "Basic summary generated"

    resp = {
        "summary": summary,
        "extractions": extractions,
        "actions": [],
        "confidence": 0.5,
        "docType": doc_type,
        "citations": []
    }
    cache_set(key, resp)
    return resp


