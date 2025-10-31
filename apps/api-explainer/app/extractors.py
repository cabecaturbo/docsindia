"""Template-based extraction engine for document processing."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

TEMPLATES_DIR = Path(__file__).parent.parent.parent.parent / "packages" / "templates" / "compiled"


class DocumentClassifier:
    """Heuristic classifier for document types."""
    
    KEYWORD_PATTERNS = {
        "credit-card-statement": [
            r"credit\s*card", r"total\s*due", r"minimum\s*payment", r"hdfc", r"icici", r"sbi"
        ],
        "bank-statement": [
            r"bank\s*statement", r"account\s*number", r"closing\s*balance", r"transaction"
        ],
        "rent-agreement": [
            r"rent\s*agreement", r"landlord", r"tenant", r"monthly\s*rent", r"security\s*deposit"
        ],
        "insurance-policy": [
            r"insurance\s*policy", r"premium", r"sum\s*assured", r"lic", r"hdfc\s*life"
        ],
        "insurance-claim": [
            r"insurance\s*claim", r"claim\s*number", r"claim\s*amount", r"pending"
        ],
        "hospital-bill": [
            r"hospital", r"patient", r"medical", r"bill", r"discharge"
        ],
        "school-circular": [
            r"school", r"circular", r"student", r"parent"
        ],
        "electricity-bill": [
            r"electricity", r"consumer\s*number", r"units", r"kwh", r"bses", r"bescom"
        ],
        "phone-bill": [
            r"mobile", r"phone\s*bill", r"airtel", r"jio", r"vi", r"data\s*used"
        ],
        "salary-slip": [
            r"salary", r"employee", r"gross", r"net\s*salary", r"deductions"
        ],
        "tax-document": [
            r"income\s*tax", r"pan", r"assessment\s*year", r"total\s*income"
        ]
    }
    
    @classmethod
    def classify(cls, text: str, type_hint: Optional[str] = None) -> str:
        """Classify document type from text content."""
        if type_hint:
            return type_hint
        
        text_lower = text.lower()
        scores = {}
        
        for doc_type, patterns in cls.KEYWORD_PATTERNS.items():
            score = sum(1 for pattern in patterns if re.search(pattern, text_lower, re.IGNORECASE))
            if score > 0:
                scores[doc_type] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "generic"


class TemplateExtractor:
    """Extract fields using compiled JSON templates."""
    
    def __init__(self):
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load compiled templates from disk."""
        if not TEMPLATES_DIR.exists():
            return
        
        for template_file in TEMPLATES_DIR.glob("*.json"):
            if template_file.name == "index.json":
                continue
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    template = json.load(f)
                    self._templates[template["id"]] = template
            except Exception:
                continue
    
    def extract(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Extract fields from text using template."""
        template = self._templates.get(doc_type)
        if not template:
            return {}
        
        extractions = {}
        citations = []
        
        fields = template.get("fields", {})
        for field_name, field_def in fields.items():
            patterns = field_def.get("patterns", [])
            
            for pattern_str in patterns:
                try:
                    pattern = re.compile(pattern_str)
                    match = pattern.search(text)
                    
                    if match:
                        value = match.group("value")
                        if value:
                            extractions[field_name] = self._normalize_value(field_name, value)
                            citations.append({
                                "field": field_name,
                                "source": f"line:{text[:match.start()].count(chr(10)) + 1}"
                            })
                            break
                except Exception:
                    continue
        
        # Apply post-rules
        self._apply_post_rules(extractions, template.get("post_rules", []))
        
        return {
            "extractions": extractions,
            "citations": citations,
            "confidence": self._calculate_confidence(extractions, len(fields))
        }
    
    def _normalize_value(self, field_name: str, value: str) -> Any:
        """Normalize extracted value based on field type."""
        # Amount fields
        if "amount" in field_name.lower() or "due" in field_name.lower() or "balance" in field_name.lower():
            # Remove currency symbols and commas
            cleaned = re.sub(r"[₹,\s]", "", value)
            try:
                return float(cleaned)
            except ValueError:
                return value
        
        # Date fields - keep as string for now
        return value.strip()
    
    def _apply_post_rules(self, extractions: Dict[str, Any], rules: List[Dict[str, Any]]):
        """Apply post-processing rules."""
        for rule in rules:
            if "ensure_amount_numeric" in rule:
                fields = rule["ensure_amount_numeric"]
                for field in fields:
                    if field in extractions:
                        value = extractions[field]
                        if isinstance(value, str):
                            cleaned = re.sub(r"[₹,\s]", "", str(value))
                            try:
                                extractions[field] = float(cleaned)
                            except ValueError:
                                pass
    
    def _calculate_confidence(self, extractions: Dict[str, Any], total_fields: int) -> float:
        """Calculate extraction confidence score."""
        if total_fields == 0:
            return 0.0
        base_confidence = len(extractions) / total_fields
        
        # Boost confidence if key fields are present
        key_fields = ["totalDue", "amount", "billAmount", "premiumAmount"]
        if any(field in extractions for field in key_fields):
            base_confidence = min(1.0, base_confidence + 0.1)
        
        return round(base_confidence, 2)


class SummaryGenerator:
    """Generate plain-language summaries from extractions."""
    
    @staticmethod
    def generate(extractions: Dict[str, Any], doc_type: str, locale: str = "en-IN") -> str:
        """Generate TL;DR summary."""
        if not extractions:
            return "Unable to extract key information from this document."
        
        if doc_type == "credit-card-statement":
            return SummaryGenerator._credit_card_summary(extractions, locale)
        elif doc_type == "bank-statement":
            return SummaryGenerator._bank_statement_summary(extractions, locale)
        elif doc_type == "rent-agreement":
            return SummaryGenerator._rent_summary(extractions, locale)
        elif doc_type == "electricity-bill":
            return SummaryGenerator._electricity_summary(extractions, locale)
        elif doc_type == "insurance-policy":
            return SummaryGenerator._insurance_policy_summary(extractions, locale)
        else:
            return SummaryGenerator._generic_summary(extractions, locale)
    
    @staticmethod
    def _credit_card_summary(extractions: Dict[str, Any], locale: str) -> str:
        parts = []
        if "totalDue" in extractions:
            amount = extractions["totalDue"]
            parts.append(f"Total amount due: ₹{amount:,.0f}" if isinstance(amount, (int, float)) else f"Total due: {amount}")
        if "dueDate" in extractions:
            parts.append(f"Due date: {extractions['dueDate']}")
        if "fees" in extractions and extractions["fees"]:
            parts.append("Late fees or charges may apply")
        return ". ".join(parts) if parts else "Credit card statement processed."
    
    @staticmethod
    def _bank_statement_summary(extractions: Dict[str, Any], locale: str) -> str:
        parts = []
        if "closingBalance" in extractions:
            balance = extractions["closingBalance"]
            parts.append(f"Closing balance: ₹{balance:,.2f}" if isinstance(balance, (int, float)) else f"Balance: {balance}")
        if "period" in extractions:
            parts.append(f"Statement period: {extractions['period']}")
        return ". ".join(parts) if parts else "Bank statement processed."
    
    @staticmethod
    def _rent_summary(extractions: Dict[str, Any], locale: str) -> str:
        parts = []
        if "monthlyRent" in extractions:
            rent = extractions["monthlyRent"]
            parts.append(f"Monthly rent: ₹{rent:,.0f}" if isinstance(rent, (int, float)) else f"Rent: {rent}")
        if "securityDeposit" in extractions:
            deposit = extractions["securityDeposit"]
            parts.append(f"Security deposit: ₹{deposit:,.0f}" if isinstance(deposit, (int, float)) else f"Deposit: {deposit}")
        if "duration" in extractions:
            parts.append(f"Agreement duration: {extractions['duration']}")
        return ". ".join(parts) if parts else "Rent agreement processed."
    
    @staticmethod
    def _electricity_summary(extractions: Dict[str, Any], locale: str) -> str:
        parts = []
        if "billAmount" in extractions:
            amount = extractions["billAmount"]
            parts.append(f"Bill amount: ₹{amount:,.2f}" if isinstance(amount, (int, float)) else f"Amount: {amount}")
        if "dueDate" in extractions:
            parts.append(f"Due date: {extractions['dueDate']}")
        if "unitsConsumed" in extractions:
            parts.append(f"Units consumed: {extractions['unitsConsumed']} kWh")
        return ". ".join(parts) if parts else "Electricity bill processed."
    
    @staticmethod
    def _insurance_policy_summary(extractions: Dict[str, Any], locale: str) -> str:
        parts = []
        if "premiumAmount" in extractions:
            premium = extractions["premiumAmount"]
            parts.append(f"Premium: ₹{premium:,.0f}" if isinstance(premium, (int, float)) else f"Premium: {premium}")
        if "dueDate" in extractions:
            parts.append(f"Due date: {extractions['dueDate']}")
        if "sumAssured" in extractions:
            sum_assured = extractions["sumAssured"]
            parts.append(f"Sum assured: ₹{sum_assured:,.0f}" if isinstance(sum_assured, (int, float)) else f"Coverage: {sum_assured}")
        return ". ".join(parts) if parts else "Insurance policy processed."
    
    @staticmethod
    def _generic_summary(extractions: Dict[str, Any], locale: str) -> str:
        key_fields = list(extractions.keys())[:3]
        if key_fields:
            return f"Document processed. Extracted: {', '.join(key_fields)}."
        return "Document processed successfully."


class ActionGenerator:
    """Generate actionable next steps."""
    
    @staticmethod
    def generate(extractions: Dict[str, Any], doc_type: str) -> List[Dict[str, Any]]:
        """Generate action checklist."""
        actions = []
        
        if doc_type == "credit-card-statement":
            if "dueDate" in extractions and "totalDue" in extractions:
                actions.append({
                    "label": "Set payment reminder",
                    "type": "reminder",
                    "payload": {"dueDate": str(extractions.get("dueDate", "")), "amount": extractions.get("totalDue")}
                })
        
        if doc_type in ["credit-card-statement", "electricity-bill", "phone-bill"]:
            if "dueDate" in extractions:
                actions.append({
                    "label": "Set payment reminder",
                    "type": "reminder",
                    "payload": {"dueDate": str(extractions.get("dueDate", ""))}
                })
        
        if doc_type == "insurance-policy":
            if "premiumDueDate" in extractions:
                actions.append({
                    "label": "Set premium payment reminder",
                    "type": "reminder",
                    "payload": {"dueDate": str(extractions.get("premiumDueDate", ""))}
                })
        
        # Always add share action
        actions.append({
            "label": "Share to WhatsApp",
            "type": "share",
            "payload": {"channel": "whatsapp"}
        })
        
        return actions

