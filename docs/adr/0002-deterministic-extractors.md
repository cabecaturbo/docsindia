# ADR-0002: Deterministic extractors first; LLM for phrasing only

**Status**: Accepted  
**Date**: 2025-11-20

## Context

Document extraction accuracy is critical. LLMs are good at phrasing but can hallucinate. We need reliable field extraction (amounts, dates, IDs) that users can trust.

## Decision

Use deterministic template-based extractors (regex/trie patterns) for field extraction. Use LLMs only for:
1. Plain-language summary phrasing (TL;DR generation)
2. Optional enhancement of action suggestions

Field extraction correctness must never depend on LLM output.

## Consequences

### Positive
- High accuracy for structured fields (amounts, dates)
- Reproducible results
- Faster processing (no LLM API calls for extraction)
- Lower cost (fewer LLM tokens)
- Easier debugging (traceable regex matches)

### Negative
- Template maintenance burden (new issuers/formats require updates)
- Less flexible for unstructured documents
- Manual template creation for each document type

### Technical Implementation
- **Templates**: YAML → JSON compilation pipeline
- **Extractors**: Regex patterns with named capture groups
- **Post-processing**: Rule-based validation (amount normalization, date parsing)
- **LLM integration**: Optional, gated by `DISABLE_LLM` flag
- **Fallback**: Generic template for unknown document types

## Alternatives Considered

1. **LLM-only extraction**: Rejected due to accuracy concerns and cost
2. **Hybrid with LLM validation**: Considered but adds complexity without clear benefit
3. **Computer vision + LLM**: Too complex for MVP; OCR → text → templates is simpler

## References

- Plan: "Deterministic extractors first"
- Templates package: `packages/templates/`

