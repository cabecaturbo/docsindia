# ADR-0004: Privacy — no image retention; anonymized text logs with rotation

**Status**: Accepted  
**Date**: 2025-11-20

## Context

User privacy is critical, especially for financial/legal documents. Regulations and user trust require minimal data retention and strong privacy guarantees.

## Decision

- **No image retention**: Images processed on-device or server-side but never stored
- **Text only**: Only extracted text sent to API
- **Cache by content hash**: Cache keyed by SHA-256 of text, not user/device
- **Anonymized logs**: PII patterns (phone, PAN) redacted before logging
- **Log rotation**: Configured at infrastructure level

## Consequences

### Positive
- Strong privacy posture
- Compliance-friendly (no permanent PII storage)
- User trust (can audit data handling)
- Lower storage costs

### Negative
- Cannot retrain models on user data
- Cannot provide document history to users
- Debugging harder (less context in logs)

### Technical Implementation
- **PII redaction**: `apps/api-explainer/app/redact.py`
- **Cache keys**: Content hash, not device ID
- **Logging**: Redacted text only
- **Image pipeline**: Process → discard immediately

## Alternatives Considered

1. **Optional image storage with consent**: Deferred (adds complexity, privacy policy updates)
2. **User accounts with explicit retention**: Out of scope for MVP
3. **Full anonymization with user IDs**: Rejected (adds complexity, not needed for MVP)

## References

- Security document: `docs/security.md`
- Privacy requirements: "No image retention; anonymized text logs"

