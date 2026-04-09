# HW2 Data Governance Reflection

**Student:** Rezo Darsavelidze
**Course:** CS-AI-2025 Spring 2026
**Assignment:** HW2 Individual Audio Pipeline

---

## Question 1: Consent Mechanisms for Real User Audio

If `hw2-audio-pipeline.py` processed real user audio instead of synthetic TTS output, the consent requirement would be significantly different from current practice.

Currently the pipeline generates audio from hardcoded text, sends it to Whisper, and transcribes it — no human voice is involved. If a real user recorded themselves and that file was sent to Whisper via OpenRouter and OpenAI, several disclosures would be required before recording begins, not after.

The consent screen would need to say, in plain language: "When you use this feature, your voice recording is sent to OpenAI for transcription. OpenAI processes it according to their API data policy [link]. Your recording is not stored by us after transcription. You can turn off this feature at any time in settings." This screen must appear before the microphone activates — not buried in a terms of service document.

Consent timing matters. A checkbox on a sign-up page four screens earlier does not constitute valid informed consent for audio collection under GDPR Article 7 — it must be contextual, meaning it appears at the moment the microphone is about to be accessed. The browser will already ask for microphone permission, but that is a technical permission, not an informed data-processing consent.

Revocation is also required. A user must be able to delete their transcript history and request that any retained data be erased. For OpenAI's API, this means directing the user to OpenAI's privacy request form, since we have no direct control over OpenAI's processing logs. That limitation must also be disclosed.

---

## Question 2: Retention Policies Across Three Scenarios

The pipeline generates two MP3 files (`voice_nova_sample.mp3`, `voice_alloy_sample.mp3`) in `audio-output/` and one JSONL cost log. The MP3 files contain synthetic speech, not a real voice — so biometric retention risk is low here. But the retention logic differs sharply for real-world applications.

**Scenario A — Study app that generates audio lessons:** The audio is synthetic TTS, generated from course content. It contains no user data. Retention policy: keep the file as long as the lesson exists in the course catalog. When a lesson is deleted, delete its audio. No personal data is involved, so no special handling is needed beyond storage cost management.

**Scenario B — Customer service transcription tool:** The audio contains a real customer's voice, which is personal data and potentially biometric data. Retention policy: delete the audio file immediately after transcription is complete. Retain the transcript for as long as the customer relationship exists (typically the duration of the support ticket plus 90 days for audit purposes), then delete. Audio and transcript must be stored separately, because transcripts are less sensitive than raw voice recordings. A customer requesting erasure under GDPR Article 17 must trigger deletion of both the transcript and any retained audio.

**Scenario C — Medical intake form:** Voice data in a medical context is doubly sensitive — it qualifies as both biometric data and health-adjacent data. Retention policy: delete audio immediately after transcription. Retain the transcript only for the legally required medical record retention period (in Georgia, medical records must be kept for a minimum period set by national health law). Any breach involving medical audio triggers mandatory notification under applicable data protection law. Encryption at rest is not optional — it is required.

---

## Question 3: PII Risks in Audio That Do Not Exist in Text

The pipeline's JSONL log (`audio-cost-log.jsonl`) records timestamps, file sizes, and cost estimates — no PII. But if the audio input were real, the risks go far beyond the words spoken.

**Voice biometrics:** A voice recording can be used to build a voiceprint — a biometric identifier unique to an individual, comparable to a fingerprint. The text "Machine learning models learn patterns from data" contains no PII. The same sentence spoken by a specific person creates a biometric record. If that audio is retained and later a voice recognition system processes it, the person can be identified even without a name attached.

**Accent and language markers:** A person's accent reveals geographic and ethnic origin — both categories that carry discrimination risk. An audio file from a Georgian speaker with a Kutaisi regional accent reveals more about that person than the text they spoke.

**Background sounds:** Audio recorded in a real environment captures ambient information — a television in the background, children's voices, traffic noise, a distinctive doorbell. Background sounds can reveal home location, household composition, and daily routines — none of which appear in a transcript.

**Emotional state inference:** Speech pace, pitch, and pauses convey stress, grief, and anger. A customer service call transcript may read as neutral while the audio reveals the customer was distressed. Emotional state inference from voice without consent is considered a high-risk processing activity under GDPR's Article 22 provisions on automated decision-making.

**Recording metadata:** The MP3 files generated by this pipeline do not embed metadata. However, real recordings often include creation timestamp, device model, and sometimes GPS coordinates in file metadata. A user who sends an audio file thinking only the content is shared may unknowingly expose their location.

---

## Question 4: Governance for Our Capstone Project

Our team's Exercise 3 decision was **Deferred Audio** — the restaurant reservation system does not include audio in the current sprint. This means the data governance burden for the MVP is low: no audio is collected, no voice data is transmitted, and no biometric risk exists.

However, the Exercise 3 roadmap identifies two post-MVP audio features: TTS confirmation readout (OpenAI reads the reservation details aloud) and STT waiter voice-memo feedback. If either feature is added, the governance requirements change substantially.

For the TTS confirmation feature: the audio is synthetic (generated from reservation data, not from the user's voice). The text sent to OpenAI contains the customer's reservation details — name, date, time, number of guests, table number. This is personal data. The privacy policy must disclose that reservation details are processed by OpenAI to generate audio. No biometric risk exists because no one's voice is involved.

For the STT waiter voice-memo feature: the waiter's voice is sent to Whisper. This is biometric data. The EPAM team would need to add a consent disclosure to the waiter onboarding flow: "When you record a feedback note, your voice is sent to OpenAI for transcription and is not retained after processing." The transcript is stored in DynamoDB in the `feedback` field of the reservation. DynamoDB encryption at rest must be enabled, which is the AWS default if KMS is configured. The waiter must be able to delete their voice notes, which maps to a DELETE endpoint on the reservation's feedback field — currently not implemented in US_7.

The most practical immediate step: enable DynamoDB KMS encryption in the Syndicate configuration now, before any sensitive data is stored. This costs nothing and protects all future data including any audio-derived transcripts.

---

*Word count: approximately 950 words.*
