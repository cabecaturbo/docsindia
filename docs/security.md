# Security & Privacy Posture

## Data Retention

### Images
- **No image retention**: Images are processed on-device (OCR) or server-side, but never stored.
- Only extracted text is sent to the API.

### Text Data
- **Ephemeral**: Text is processed and cached, but not permanently stored.
- Cache TTL: 30 days (configurable via `CACHE_TTL_DAYS`).
- Cache keyed by content hash (SHA-256), not by user/device.

### Logs
- **Anonymized**: PII-like patterns (phone numbers, PAN) are redacted before logging.
- Log rotation: Configured at infrastructure level.
- No structured user data in logs.

## PII Redaction

The following patterns are automatically redacted from logs:

- **Phone numbers**: Indian mobile patterns (`(?:\+?91[- ]?)?[6-9]\d{9}`)
- **PAN**: Format `[A-Z]{5}[0-9]{4}[A-Z]`

Redaction is performed server-side before any logging occurs.

## Rate Limiting

- **Per-device**: Rate limiting based on `deviceId` in requests.
- Default: 60 requests per minute per device.
- Implemented via Redis (sliding window per minute).
- Returns `429 Too Many Requests` when exceeded.

## Secrets Management

- **Environment variables only**: All secrets (API keys, Redis URLs, etc.) via environment variables.
- **No secrets in repo**: `.gitignore` excludes `.env` files.
- **Production**: Railway/cloud provider secrets management.

## API Security

- **CORS**: Configurable origins (default: `*` for development).
- **Request validation**: Pydantic models validate all inputs.
- **Request IDs**: Every request gets a unique ID for tracing.

## Android App

- **Permissions**: Camera, storage (for PDF import only).
- **Local data**: OCR results and summaries stored locally only.
- **Network**: HTTPS only; certificate pinning considered for production.

## Watermarking

- Shared content (WhatsApp, exports) includes "For learning" watermark.
- Indicates educational/non-legal nature of summaries.

## Compliance Considerations

- **No GDPR requirement**: MVP targets India only.
- **Data minimization**: Only necessary text processed.
- **No user accounts**: MVP operates on device ID basis.

## Future Enhancements

- End-to-end encryption for sensitive documents
- Optional user accounts with explicit consent
- Regional data residency requirements

