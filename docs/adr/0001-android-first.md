# ADR-0001: Android-first, WhatsApp-native sharing

**Status**: Accepted  
**Date**: 2025-11-20

## Context

Target users in India are primarily Android users. WhatsApp is the dominant messaging platform and primary sharing channel for document explanations.

## Decision

Build Android app first; defer iOS development. Optimize share flows specifically for WhatsApp integration.

## Consequences

### Positive
- Faster time-to-market (single platform)
- Focused development on Android ecosystem
- Deep WhatsApp integration (native share intents, deep links)
- Lower initial development cost

### Negative
- iOS users excluded from MVP
- Potential market share loss to iOS users
- Future iOS development requires separate effort

### Technical Implementation
- **Kotlin** for Android app
- **CameraX** for camera capture
- **ML Kit Text Recognition v2** for on-device OCR
- WhatsApp share intents with pre-filled text
- Deep linking support for referral flows

## Alternatives Considered

1. **React Native/Flutter**: Rejected due to OCR performance concerns and native API access needs
2. **iOS-first**: Rejected due to smaller market share in target demographics
3. **Desktop-first**: Rejected as non-goal for MVP

## References

- Product brief: Android-first consumer app
- Distribution strategy: WhatsApp-native sharing

