import re


_PHONE = re.compile(r"(?<!\d)(?:\+?91[- ]?)?[6-9]\d{9}(?!\d)")
_PAN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")


def redact_text(text: str) -> str:
    redacted = _PHONE.sub("[REDACTED_PHONE]", text)
    redacted = _PAN.sub("[REDACTED_PAN]", redacted)
    return redacted


