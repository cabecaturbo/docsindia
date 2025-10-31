from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any
from fastapi import HTTPException
from ..cache import cache_get, cache_set, content_hash, rate_limit_allow
from ..extractors import DocumentClassifier, TemplateExtractor, SummaryGenerator, ActionGenerator


router = APIRouter()

# Initialize extractors
_extractor = TemplateExtractor()


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
    if not text:
        raise HTTPException(status_code=400, detail="Document text is required")
    
    # Check cache
    key = f"explain:{content_hash(text)}"
    cached = cache_get(key)
    if cached:
        return cached
    
    # Classify document type
    doc_type = DocumentClassifier.classify(text, req.docMeta.typeHint)
    
    # Extract fields using templates
    extraction_result = _extractor.extract(text, doc_type)
    extractions = extraction_result["extractions"]
    citations = extraction_result["citations"]
    confidence = extraction_result["confidence"]
    
    # Generate summary
    summary = SummaryGenerator.generate(extractions, doc_type, req.locale)
    
    # Generate actions
    actions = ActionGenerator.generate(extractions, doc_type)
    
    resp = {
        "summary": summary,
        "extractions": extractions,
        "actions": actions,
        "confidence": confidence,
        "docType": doc_type,
        "citations": citations
    }
    
    cache_set(key, resp)
    return resp


