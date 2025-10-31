# SimpleDoc MVP Plan (30 days)

## Product Overview

SimpleDoc is an Android-first consumer app that explains everyday Indian documents in plain language. Users upload photos/PDFs → get key field extractions → receive a plain-language summary → see actionable next steps → share to WhatsApp.

## Target Users

- Households in India (parents, tenants, salaried professionals)
- Primary distribution: Android + WhatsApp-native sharing

## MVP Scope (30 days)

### Core Features

1. **Document Upload & Processing**
   - Camera capture or PDF import
   - On-device OCR (ML Kit Text Recognition v2)
   - Server-side extraction fallback for complex PDFs

2. **Document Types (v1)**
   - Bank/credit card statements (fees, due dates)
   - Insurance policy/claim checklists
   - Rent agreements (red flags)
   - Hospital bills
   - School circulars
   - Additional: electricity, phone, salary, tax documents

3. **Languages**
   - English + Hindi at MVP
   - Regional languages (2-3) post-MVP

4. **Output**
   - Single-page summary (TL;DR)
   - Key field extractions
   - "What to do next" actions
   - WhatsApp share with watermark

### Monetization

- **Free tier**: Single-page summary
- **Paid tier**: ₹149/mo, ₹999/yr
  - Multi-page documents
  - PDF exports
  - Payment reminders
  - Premium templates
  - Family plan features
- **Referral**: Give 7 days, get 7 days via WhatsApp share

### Non-Goals (MVP)

- Full legal/financial advice engine
- Enterprise workflows
- Desktop parity
- iOS app

## Milestones

### Week 1
- ✅ Monorepo scaffold
- ✅ Android camera/PDF import + OCR stubs
- ✅ FastAPI `/health`
- ✅ 2 extractors (credit card, bank)
- ⏳ WhatsApp share

### Week 2
- ✅ `/explain` pipeline (classifier → extractors → red-flags → TL;DR)
- ⏳ Hindi localization
- ✅ Redis cache
- ⏳ Analytics
- ✅ +6 templates (12 total)

### Week 3
- ⏳ Paywall + referral
- ⏳ Reminders
- ⏳ Export PDF
- ⏳ QA on 10 real docs

### Week 4
- ⏳ Polish
- ⏳ CI setup
- ⏳ Privacy policy
- ⏳ Creator toolkit
- ⏳ Launch prep

## KPIs (First 30-45 days)

- D1 retention ≥ 30%
- D7 retention ≥ 15%
- Free→Paid conversion: 2-4%
- CAC: ₹40-₹120 (creators/WhatsApp groups)
- Median explain latency < 3.5s (single page)
- Refunds < 3%

## Architecture Decisions

See `adr/` directory for:
- ADR-0001: Android-first, WhatsApp-native
- ADR-0002: Deterministic extractors first; LLM for phrasing only
- ADR-0003: Subscriptions via Play Billing; referral unlocks (7-day)
- ADR-0004: Privacy — no image retention; anonymized text logs with rotation

## Technology Stack

- **Android**: Kotlin, CameraX, ML Kit, Play Billing v6
- **Backend**: FastAPI, Python 3.11, Redis
- **Deploy**: Railway (API + Redis)
- **Templates**: YAML → JSON compiler

## Risks & Mitigations

- **OCR variability** → Deterministic extractors with fuzzy post-rules; conservative confidence scoring
- **PDF parsing on low-end devices** → Server extraction fallback with guardrails
- **Latency target <3.5s** → Aggressive caching by content hash; short templates; on-device OCR

