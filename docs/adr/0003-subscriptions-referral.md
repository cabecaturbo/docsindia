# ADR-0003: Subscriptions via Play Billing; referral unlocks (7-day)

**Status**: Accepted  
**Date**: 2025-11-20

## Context

MVP monetization model: free single-page, paid multi-page + exports + reminders. Need referral mechanism to drive growth via WhatsApp sharing.

## Decision

- Use **Google Play Billing Library v6** for subscriptions
- Pricing: ₹149/month, ₹999/year
- Referral: Give 7 days, get 7 days (unlocked via WhatsApp share with referral code)
- Free tier limits enforced client-side and server-side

## Consequences

### Positive
- Native Play Store integration
- Automated subscription management
- Built-in family sharing support (future)
- Referral drives viral growth via WhatsApp

### Negative
- Android-only (iOS would need different billing)
- Google's 15-30% commission
- Referral code management complexity

### Technical Implementation
- **Play Billing v6**: Subscription products (monthly/yearly)
- **Server validation**: Verify purchase tokens server-side
- **Referral codes**: Generate unique codes per user share
- **Trial periods**: 7-day unlock for referrer and referee
- **Client limits**: Free tier restricted to single-page documents

## Alternatives Considered

1. **One-time payments**: Rejected (recurring revenue better)
2. **External payment gateway**: Rejected (complexity, Play Store policies)
3. **Longer referral periods**: Rejected (7 days balances growth vs. revenue)

## References

- Monetization plan: ₹149/mo, ₹999/yr
- Referral: "give 7 days, get 7 days"

