# Exercise 3: Audio Decision for Capstone

**Team Name:** team-3, run-21
**Team Members:** Rezo Darsavelidze, Bohdan, Nino, Oleksandr
**Date:** 09 April 2026

---

## Your Capstone Product

**Product name:** Restaurant Reservation System
**One-sentence description:** A serverless restaurant reservation platform that lets customers book tables online and enables waiters to manage reservations through a dashboard, built on AWS Lambda, DynamoDB, and API Gateway.

---

## Audio Decision

Select one:

- [ ] **Core audio** -- our product cannot function without TTS/STT
- [ ] **Enhancement audio** -- audio adds value but is not required for core functionality
- [x] **Deferred audio** -- audio would be nice but is not worth the complexity right now
- [ ] **No audio** -- audio does not fit our product

---

## Reasoning

### If you selected Deferred Audio or No Audio:

**Why audio does not fit right now:**

Our product's core workflow is form-driven: a customer selects a date, time, and party size; the system checks availability against DynamoDB; the reservation is confirmed and assigned to a waiter. None of these steps benefit from voice input or output at the current MVP stage. The team is mid-sprint on US_7 (Waiter Reservations Dashboard) and US_8 (visitor reservation support). Introducing a new API surface — OpenRouter TTS/STT, audio file storage in S3, and client-side microphone permissions — before these user stories are stable adds engineering risk without corresponding user value.

The 90-minute fixed reservation and 15-minute gap logic (US_6) is already complex. Adding audio routing before the core booking rules are fully tested would make debugging significantly harder. Audio also requires the frontend (Bohdan) to implement browser microphone access, which is a nontrivial UI change not scoped for the current sprint.

"We don't have time" is not the reason. The reason is that no current user story requires audio, and introducing it now would increase the defect surface area without delivering a feature that customers have asked for.

**What would change your decision:**

Three specific conditions would cause us to reconsider:

1. A stakeholder explicitly requests an accessibility feature — for example, a visually impaired customer who needs reservation confirmation read aloud. This would move us to Enhancement Audio (TTS only, no STT).
2. The waiter feedback feature (currently a text field) proves hard to use in a noisy restaurant — waiters prefer speaking a note rather than typing. This would trigger STT for the feedback field only.
3. The product pivots to handle phone-in reservations, requiring the system to transcribe a customer's spoken request into a structured reservation. This would require full STT with structured output extraction — a significantly larger engineering effort.

**Alternative to audio:**

For customers who want a lower-friction interaction, we offer a Telegram or WhatsApp bot integration (planned for post-MVP) where they send a text message and the system books the reservation. This gives mobile-first users an interaction that feels more natural than a web form, without requiring voice processing or microphone permissions.

---

## Impact on Design Review

**Does this decision change anything in your submitted Design Review?**

- [ ] No change needed -- Design Review already reflects this decision
- [x] Yes -- we need to update the feature roadmap to include/exclude audio
- [ ] Yes -- we need to update the architecture diagram
- [ ] Yes -- we need to update the data governance section

**Specific update needed (if any):**

The feature roadmap should explicitly list audio as a deferred post-MVP feature with the two trigger conditions above (accessibility request; waiter feedback usability issue). The current Design Review does not mention audio at all — adding it to the roadmap table with "Deferred" status and a clear trigger condition makes the decision visible and intentional rather than an omission.

---

## Post-MVP Audio Roadmap

| Phase | Feature | Trigger |
|-------|---------|---------|
| MVP (current) | No audio | — |
| Post-MVP v2 | Reservation confirmation TTS (nova voice) | Accessibility requirement confirmed |
| Post-MVP v2 | Waiter voice-memo feedback via STT | Feedback usability issue validated |
| Future | Real-time voice reservation (phone-in flow) | Business decides to target call-in customers |

---

## Estimated Cost (if we did add audio)

Based on Exercise 1 and 2 results:

| Feature | Usage estimate | Daily cost |
|---------|---------------|------------|
| Confirmation TTS (168 chars per booking) | 50 bookings/day | ~$0.13 |
| Waiter voice memo STT (15 s avg per note) | 30 notes/day | ~$0.045 |
| **Total** | | **~$0.18/day (~$5.40/month)** |

Audio cost is negligible at this scale. The decision against audio is not driven by cost but by engineering scope and sprint priority.

---

## Team Agreement

All team members present agree with this decision:

| Name | Agree? |
|------|--------|
| Rezo Darsavelidze | [x] Yes |
| Bohdan | [x] Yes |
| Nino | [x] Yes |
| Oleksandr | [x] Yes |

---

*Save this file and commit it to your team repository before the end of lab.*
