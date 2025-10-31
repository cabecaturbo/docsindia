# API Contracts

## Base URL

Production: TBD (Railway deployment)  
Development: `http://localhost:8000`

## Endpoints

### POST /health

Health check endpoint.

**Request:**
```json
{}
```

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

---

### POST /explain

Explain a document by extracting key fields and generating a plain-language summary.

**Request:**
```json
{
  "docText": "HDFC Credit Card Statement ...",
  "docMeta": {
    "typeHint": "credit-card-statement",
    "pages": 2
  },
  "locale": "en-IN",
  "hints": false,
  "deviceId": "abc123"
}
```

**Request Schema:**
- `docText` (string, required): Normalized document text (min length 1)
- `docMeta` (object, required):
  - `typeHint` (string, optional): Suggested document type
  - `pages` (integer, optional, min 1): Number of pages
- `locale` (string, required): Locale code (pattern: `^[a-z]{2}-[A-Z]{2}$`, e.g., `en-IN`, `hi-IN`)
- `hints` (boolean, optional): Whether to include hints (default: false)
- `deviceId` (string, required): Unique device identifier (min length 3)

**Response:**
```json
{
  "summary": "You were charged a late fee of ₹500. Total due ₹4,250 by 15 Nov.",
  "extractions": {
    "issuer": "HDFC",
    "totalDue": 4250,
    "dueDate": "2025-11-15",
    "fees": [
      {"label": "Late fee", "amount": 500}
    ]
  },
  "actions": [
    {
      "label": "Set payment reminder",
      "type": "reminder",
      "payload": {"dueDate": "2025-11-15"}
    },
    {
      "label": "Dispute late fee (template)",
      "type": "template",
      "payload": {"channel": "email"}
    }
  ],
  "confidence": 0.92,
  "docType": "credit-card-statement",
  "citations": [
    {"field": "totalDue", "source": "page1:line42"}
  ]
}
```

**Response Schema:**
- `summary` (string, required): Plain-language summary
- `extractions` (object, required): Key field extractions (document-type specific)
- `actions` (array, required): Actionable next steps
  - `label` (string, required): Action label
  - `type` (string, required): Action type (e.g., `reminder`, `template`)
  - `payload` (object, required): Action-specific data
- `confidence` (number, required): Confidence score (0-1)
- `docType` (string, required): Detected document type
- `citations` (array, required): Source references for extracted fields
  - `field` (string, required): Field name
  - `source` (string, required): Source location (e.g., `page1:line42`)

**Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid request (validation error)
- `422 Unprocessable Entity`: Unsupported document type
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

**Rate Limiting:**
- Default: 60 requests per minute per `deviceId`
- Configurable via `RATE_LIMIT_RPM` environment variable

**Caching:**
- Responses cached by content hash (SHA-256 of normalized text)
- TTL: 30 days (configurable via `CACHE_TTL_DAYS`)

---

### GET /templates

List all supported document types and their versions.

**Request:**
```
GET /templates
```

**Response:**
```json
{
  "docTypes": [
    {
      "id": "credit-card-statement",
      "version": "1.0.0",
      "issuers": ["HDFC", "ICICI", "SBI"]
    },
    {
      "id": "bank-statement",
      "version": "1.0.0",
      "issuers": ["HDFC", "ICICI", "SBI"]
    }
  ]
}
```

**Response Schema:**
- `docTypes` (array, required): List of document types
  - `id` (string, required): Document type ID
  - `version` (string, required): Template version
  - `issuers` (array, optional): List of known issuers

**Status Codes:**
- `200 OK`: Success

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

**Error Codes:**
- `ERR_VALIDATION` (400): Request validation failed
- `ERR_RATE_LIMIT` (429): Too many requests
- `ERR_UNSUPPORTED_DOC` (422): Unsupported document type
- `ERR_INTERNAL` (500): Internal server error

## Headers

### Request Headers
- `Content-Type: application/json` (required for POST requests)

### Response Headers
- `x-request-id`: Unique request identifier for tracing
- `x-response-time-ms`: Response time in milliseconds

