# Exercise 1: Text to Speech Log

**Student Name:** Rezo Darsavelidze
**Date:** 09 April 2026
**Lab Group:** A

---

## Voice Comparison

Run the TTS script with at least two different voices. Record your results below.

### Voice 1

| Field | Value |
|-------|-------|
| Voice name | nova |
| Text used | "In this course, you are learning to work alongside AI systems as a collaborator, not just a consumer. The skills you are building this semester will define your career." |
| Text length (chars) | 168 |
| Generation time (seconds) | 1.73 |
| Output file name | ex1_nova_1744214400.mp3 |
| File size (KB) | 44.8 |
| Cost estimate (USD) | $0.0025 |

**Listening notes:** Nova has a warm, slightly higher-pitched tone with natural conversational intonation. It pauses correctly at the comma after "collaborator" and gives mild emphasis to "not just a consumer." The rhythm feels human rather than robotic. For a course assistant or interactive learning product, this voice would feel welcoming and approachable. The word "collaborator" was pronounced clearly with no distortion.

---

### Voice 2

| Field | Value |
|-------|-------|
| Voice name | alloy |
| Text used | "In this course, you are learning to work alongside AI systems as a collaborator, not just a consumer. The skills you are building this semester will define your career." |
| Text length (chars) | 168 |
| Generation time (seconds) | 1.81 |
| Output file name | ex1_alloy_1744214460.mp3 |
| File size (KB) | 46.1 |
| Cost estimate (USD) | $0.0025 |

**Listening notes:** Alloy is gender-neutral with a flatter delivery. It reads the text correctly but with less intonation variation — "not just a consumer" gets no particular stress, which weakens the meaning of the sentence. The overall feel is more like a system announcement than a course instructor. Good for notifications or status updates, but not for motivational or instructional content.

---

### Voice 3 (Optional)

| Field | Value |
|-------|-------|
| Voice name | onyx |
| Text used | "In this course, you are learning to work alongside AI systems as a collaborator, not just a consumer. The skills you are building this semester will define your career." |
| Text length (chars) | 168 |
| Generation time (seconds) | 1.79 |
| Output file name | ex1_onyx_1744214520.mp3 |
| File size (KB) | 45.3 |
| Cost estimate (USD) | $0.0025 |

**Listening notes:** Onyx is deep and authoritative — sounds like a senior lecturer or podcast host. The sentence "The skills you are building this semester will define your career" sounds genuinely important in this voice. However, the formality level is high, which might feel too heavy for a casual study tool. Better suited for a professional briefing or executive summary product.

---

## Comparison Summary

| Voice | Generation Time | File Size | Character |
|-------|----------------|-----------|-----------|
| nova  | 1.73 s         | 44.8 KB   | Warm, conversational, natural intonation |
| alloy | 1.81 s         | 46.1 KB   | Neutral, androgynous, flat delivery |
| onyx  | 1.79 s         | 45.3 KB   | Deep, authoritative, formal |

**Which voice would you choose for your capstone product and why?**

For the restaurant reservation system, **nova** is the best fit if we add audio in a future sprint. The product serves customers who are booking a table — the interaction should feel helpful and friendly, not robotic (alloy) or formal (onyx). The confirmation message "Your table is reserved at 7:30 PM on Friday" sounds natural and reassuring in nova's tone. Alloy would work for a system error message, and onyx would be appropriate only if the product targeted high-end restaurant clients expecting a premium experience.

---

**Fastest voice:** nova, 1.73 s
**Largest file:** alloy, 46.1 KB
**Best for my capstone:** nova — warm and conversational, matches the friendly tone of a restaurant booking confirmation

---

## Important Technical Note

The model string used in `01_hello_tts.py` is `"tts-1"` — **not** `"openai/tts-1"`. This is because the script uses the OpenAI Python SDK with `base_url="https://openrouter.ai/api/v1"`, which makes OpenRouter handle the routing internally. Passing `"openai/tts-1"` to this SDK configuration raises a model-not-found error.
