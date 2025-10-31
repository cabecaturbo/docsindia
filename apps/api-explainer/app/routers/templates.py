from fastapi import APIRouter
from typing import Any
import json
from pathlib import Path


router = APIRouter()

# Load templates index
TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent.parent / "packages" / "templates" / "compiled"
INDEX_PATH = TEMPLATES_DIR / "index.json"


@router.get("/templates")
def get_templates() -> dict[str, Any]:
    """List all supported document types and versions."""
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Fallback: return empty index if compiled templates not available
    return {"docTypes": []}

