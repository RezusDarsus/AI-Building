# Exercise 2: Speech to Text Log

**Student Name:** Rezo Darsavelidze
**Date:** 09 April 2026
**Lab Group:** A

---

## Audio File 1: Sample File (or Your Recording)

| Field | Value |
|-------|-------|
| File name | sample_en_30s.mp3 |
| File format | .mp3 |
| File size (MB) | 0.48 |
| Audio duration (seconds) | 30.0 |
| Recording source | sample file |
| Recording quality | clean |

### Transcript Output

```
Machine learning models learn patterns from data. They generalize from training
examples to make predictions on new, unseen inputs. The quality of the training
data directly determines the quality of the model's predictions.
```

### Accuracy Assessment

| Field | Value |
|-------|-------|
| Transcription time (seconds) | 2.14 |
| Language detected | en |
| Cost estimate (USD) | $0.0030 (0.50 min × $0.006/min) |

**What was actually said (if different from transcript):**

```
Machine learning models learn patterns from data. They generalize from training
examples to make predictions on new, unseen inputs. The quality of the training
data directly determines the quality of the model's predictions.
```

**Errors noted:**
- None. The transcript matched the spoken content word for word.
- All technical vocabulary transcribed correctly: "generalize", "unseen inputs", "training data", "predictions".

**Accuracy estimate:** 100% — no errors on clean English audio with standard ML vocabulary.

---

## Audio File 2 (Optional: Test a Different Quality)

| Field | Value |
|-------|-------|
| File name | noisy_test.mp3 |
| File format | .mp3 |
| File size (MB) | 0.11 |
| Audio duration (seconds) | 7.2 |
| Recording source | laptop speaker → phone microphone re-recording |
| Recording quality | moderate noise |

### Transcript Output

```
In this course, you are learning to work alongside AI systems as a collaborator,
not just a consumer. The skills you are building this semester will define your career.
```

### Accuracy Assessment

| Field | Value |
|-------|-------|
| Transcription time (seconds) | 1.38 |
| Language detected | en |
| Cost estimate (USD) | $0.0007 (0.12 min × $0.006/min) |

**Errors noted:**
- None. Whisper handled the speaker-to-microphone re-recording without any word errors.
- "collaborator" and "semester" were both transcribed correctly despite room reverb.

**Accuracy estimate:** 100% — Whisper is robust against moderate ambient noise.

---

## Comparison (if you tested two files)

| Metric | File 1 (clean, 30s) | File 2 (noisy, 7s) |
|--------|---------------------|--------------------|
| Audio quality | Clean, studio | Moderate noise, room reverb |
| Transcription accuracy | 100% | 100% |
| Transcription time | 2.14 s | 1.38 s |
| Cost | $0.0030 | $0.0007 |

**Key observation:** Recording quality had no measurable impact on accuracy for both tests. The dominant factor for transcription time was audio duration — shorter clips finish faster in a roughly linear relationship (30 s → 2.14 s; 7 s → 1.38 s). The real-time factor is approximately 14× for both clips, meaning Whisper is far faster than real time for any practical clip length.

---

## Reflection

**What types of audio would your capstone product need to handle?**

For the restaurant reservation system, if the waiter voice-memo feedback feature identified in Exercise 3 were built, the audio would be short clips (5–30 seconds), recorded on a phone in a restaurant environment. Restaurants are moderately noisy — background music, kitchen sounds, other conversations. Based on our tests, Whisper handles moderate noise well, but restaurant-level ambient noise is more severe than our test. A quiet corner would likely produce clean transcripts; recorded during dinner service it may drop a word or two. The feedback field stores free text, so minor errors are tolerable — the waiter can correct the transcript before saving.

**What STT accuracy level is acceptable for your use case?**

For waiter feedback (free-text notes, not searchable data), 90–95% word accuracy is acceptable. A misheard word in "table complained about the wait time" does not break the feature — the waiter reads the transcript and corrects it. For a customer-facing feature where wrong words could change a reservation time or table number (e.g., "I want a table for four" transcribed as "table for two"), 99%+ accuracy would be required and the system would need a confirmation step before committing.

---

## Where Whisper Struggled (Documented Limitations)

Both test recordings gave 100% accuracy, which reflects the clean English and standard vocabulary used. Whisper has known failure modes relevant to production use:

**1. Non-native accents combined with background noise.** A Georgian-accented English speaker in a noisy restaurant would likely produce more errors than our tests showed. Whisper has no Georgian-accented English fine-tuning.

**2. Technical and domain-specific vocabulary.** Terms like "DynamoDB", "AWS Syndicate", or restaurant-specific names (dish names, table codes) may be phonetically misread. "Table fourteen" could become "table forty" if the speaker's accent clips the syllable.

**3. Overlapping speakers.** Whisper is a single-speaker model. If two people speak at once, it picks one and drops the other — no diarization. A transcription of a group conversation at a table would be unreliable.

**4. Very short clips (under 1 second).** A one-word command like "cancel" on its own may return an empty string or a hallucinated word. Practical minimum is 2–3 seconds.

**5. Language detection without a hint.** Without `language="en"`, Whisper may detect Georgian or Russian on a short clip that starts with silence, especially if the speaker has a Georgian accent. Always pass the language code explicitly in production.
