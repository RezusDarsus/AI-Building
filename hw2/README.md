# HW2 – Audio Pipeline

A complete TTS → STT round-trip pipeline using OpenAI TTS and Whisper directly via the OpenAI API.

## What It Does

Takes a hardcoded text string, generates MP3 audio with two voices (nova and alloy),
transcribes the nova output back to text using Whisper, compares original vs transcript
with word-overlap accuracy, and prints a full cost and latency summary.

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Run

```bash
python hw2-audio-pipeline.py
```

## Expected Output

```
=== HW2 Audio Pipeline ===

[1/4] Generating speech with voice: nova
  Text: "Machine learning models learn patterns from data. They gene..."
  Generated in 2.14s
  File: audio-output/voice_nova_sample.mp3 (47.3 KB)
  Cost: $0.0021

[2/4] Generating speech with voice: alloy
  Text: "Machine learning models learn patterns from data. They gene..."
  Generated in 1.98s
  File: audio-output/voice_alloy_sample.mp3 (45.8 KB)
  Cost: $0.0021

[3/4] Transcribing audio-output/voice_nova_sample.mp3
  File: voice_nova_sample.mp3
  Transcript: "Machine learning models learn patterns from data. They ..."
  Transcribed in 1.52s
  Audio duration: 8.3s
  Cost: $0.0008

[4/4] Comparing original vs transcribed text
  Original:    "Machine learning models learn patterns from data. They gene..."
  Transcribed: "Machine learning models learn patterns from data. They gene..."
  Word overlap accuracy: 100.0%

=== Cost and Latency Summary ===
  TTS calls:  2 | Total cost: $0.0042 | Avg latency: 2.06s
  STT calls:  1 | Total cost: $0.0008 | Avg latency: 1.52s
  Pipeline total: $0.0050

  Cost log: audio-cost-log.jsonl

  If your product processes 100 passages/day:
    Daily cost:  ~$0.50
    Monthly:     ~$15.00

=== Pipeline complete ===
```

## Files

| File | Description |
|------|-------------|
| `hw2-audio-pipeline.py` | Main pipeline script |
| `reflection.md` | Data governance reflection (950 words) |
| `requirements.txt` | Python dependencies |
| `.env.example` | API key template |
| `audio-output/` | Generated MP3 files |
| `audio-cost-log.jsonl` | Per-call cost log (created at runtime) |
