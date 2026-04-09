

import os
import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

load_dotenv()

logging.basicConfig(level=logging.WARNING)   # suppress SDK debug noise

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


TTS_MODEL = "tts-1"
STT_MODEL = "whisper-1"

SUPPORTED_FORMATS = {".mp3", ".mp4", ".wav", ".webm", ".m4a", ".mpeg", ".mpga"}
MAX_FILE_MB = 25

OUTPUT_DIR = Path("audio-output")
OUTPUT_DIR.mkdir(exist_ok=True)

COST_LOG = Path("audio-cost-log.jsonl")

TTS_COST_PER_1K_CHARS = 0.015   # $0.015 per 1,000 characters
STT_COST_PER_MINUTE   = 0.006   # $0.006 per minute of audio

_session = {
    "tts_calls": 0, "tts_total_cost": 0.0, "tts_total_latency": 0.0,
    "stt_calls": 0, "stt_total_cost": 0.0, "stt_total_latency": 0.0,
}



def _log_call(call_type: str, model: str, duration_s: float,
              input_size: str, cost: float, meta: dict = None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "call_type": call_type,
        "model": model,
        "duration_seconds": duration_s,
        "input_size": input_size,
        "cost_estimate_usd": round(cost, 6),
        "metadata": meta or {},
    }
    with open(COST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    if call_type == "tts":
        _session["tts_calls"] += 1
        _session["tts_total_cost"] += cost
        _session["tts_total_latency"] += duration_s
    else:
        _session["stt_calls"] += 1
        _session["stt_total_cost"] += cost
        _session["stt_total_latency"] += duration_s


# ── TTS ────────────────────────────────────────────────────────────────────

def text_to_speech(text: str, voice: str, output_filename: str,
                   step_label: str = "") -> dict:
    """
    Generate an MP3 file from text using tts-1 via the OpenAI API.

    Handles:
    - RateLimitError  → one automatic retry after 10 s, then re-raises
    - APIConnectionError → one automatic retry after 2 s, then re-raises
    - APIError → prints error details, re-raises
    """
    valid_voices = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}
    if voice not in valid_voices:
        raise ValueError(f"Unknown voice '{voice}'. Valid: {valid_voices}")
    if not text.strip():
        raise ValueError("text must not be empty")

    output_path = OUTPUT_DIR / output_filename

    if step_label:
        print(f"\n{step_label}")
    print(f"  Text: \"{text[:60]}...\"")

    cost = (len(text) / 1000) * TTS_COST_PER_1K_CHARS

    for attempt in range(1, 3):   # up to 2 attempts
        try:
            start = time.time()
            with client.audio.speech.with_streaming_response.create(
                model=TTS_MODEL,
                voice=voice,
                input=text,
                response_format="mp3",
            ) as response:
                response.stream_to_file(str(output_path))
            elapsed = round(time.time() - start, 2)
            break
        except RateLimitError:
            if attempt == 1:
                print(f"  Rate limit hit. Retrying in 10s...")
                time.sleep(10)
                continue
            print("  Rate limit hit on retry. Check your OpenAI billing/quota at platform.openai.com.")
            raise
        except APIConnectionError:
            if attempt == 1:
                print(f"  Connection error on attempt {attempt}. Retrying in 2s...")
                time.sleep(2)
                continue
            print("  Connection error on retry. Check your network and API key.")
            raise
        except APIError as e:
            print(f"  API error: {e}")
            raise

    size_kb = output_path.stat().st_size / 1024
    _log_call("tts", TTS_MODEL, elapsed, f"{len(text)} chars", cost,
              {"voice": voice, "output_file": output_filename})

    print(f"  Generated in {elapsed}s")
    print(f"  File: {output_path} ({size_kb:.1f} KB)")
    print(f"  Cost: ${cost:.4f}")

    return {
        "output_path": str(output_path),
        "generation_time_seconds": elapsed,
        "file_size_bytes": output_path.stat().st_size,
        "voice": voice,
        "text_length_chars": len(text),
        "cost_estimate": cost,
    }


# ── STT ────────────────────────────────────────────────────────────────────

def speech_to_text(audio_file_path: str, step_label: str = "") -> dict:
    """
    Transcribe an audio file using whisper-1 via the OpenAI API.

    Validates: file existence, format, and size before calling the API.
    Handles: RateLimitError, APIConnectionError (1 retry), APIError.
    Saves the transcript as a .txt file alongside the audio file.
    """
    path = Path(audio_file_path)

    # ── Pre-flight checks (fail fast with clear messages) ──────────────
    if not path.exists():
        print(f"  Error: File not found: {audio_file_path}")
        print("  Check the path and try again.")
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"  Error: Unsupported format '{path.suffix}'.")
        print(f"  Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        raise ValueError(f"Unsupported audio format: {path.suffix}")

    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        print(f"  Error: File too large ({size_mb:.1f} MB). Maximum: {MAX_FILE_MB} MB.")
        print("  Trim to under 30 seconds using pydub or ffmpeg.")
        raise ValueError(f"File too large: {size_mb:.1f} MB")

    if step_label:
        print(f"\n{step_label}")
    print(f"  File: {path.name}")

    for attempt in range(1, 3):
        try:
            start = time.time()
            with open(path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=STT_MODEL,
                    file=audio_file,
                    response_format="verbose_json",
                )
            elapsed = round(time.time() - start, 2)
            break
        except RateLimitError:
            if attempt == 1:
                print(f"  Rate limit hit. Retrying in 10s...")
                time.sleep(10)
                continue
            print("  Rate limit hit on retry. Check your OpenAI billing/quota at platform.openai.com.")
            raise
        except APIConnectionError:
            if attempt == 1:
                print(f"  Connection error on attempt {attempt}. Retrying in 2s...")
                time.sleep(2)
                continue
            print("  Connection error on retry. Check your network and API key.")
            raise
        except APIError as e:
            print(f"  API error: {e}")
            raise

    duration_s = getattr(transcript, "duration", None)
    duration_min = (duration_s or 30) / 60
    cost = duration_min * STT_COST_PER_MINUTE

    _log_call("stt", STT_MODEL, elapsed, f"{size_mb:.1f} MB", cost,
              {"audio_duration_seconds": duration_s,
               "language": getattr(transcript, "language", "unknown")})

    # Save transcript to a .txt file next to the audio file
    transcript_path = OUTPUT_DIR / (path.stem + "_transcript.txt")
    transcript_path.write_text(transcript.text, encoding="utf-8")

    print(f"  Transcript: \"{transcript.text[:80]}...\"")
    print(f"  Saved to: {transcript_path}")
    print(f"  Transcribed in {elapsed}s")
    if duration_s:
        print(f"  Audio duration: {duration_s:.1f}s")
    print(f"  Cost: ${cost:.4f}")

    return {
        "text": transcript.text,
        "language": getattr(transcript, "language", "en"),
        "duration_seconds": duration_s,
        "transcription_time_seconds": elapsed,
        "file_name": path.name,
        "file_size_mb": round(size_mb, 2),
        "cost_estimate": cost,
        "transcript_path": str(transcript_path),
    }


# ── Comparison ─────────────────────────────────────────────────────────────

def compare_texts(original: str, transcribed: str) -> dict:
    """Word-level overlap comparison (same method as 03_capstone_audio_example.py)."""
    original_words    = original.lower().split()
    transcribed_words = transcribed.lower().split()
    original_set      = set(original_words)
    transcribed_set   = set(transcribed_words)
    overlap           = original_set & transcribed_set
    accuracy = len(overlap) / len(original_set) if original_set else 0
    return {
        "word_overlap_accuracy": round(accuracy * 100, 1),
        "original_word_count":   len(original_words),
        "transcribed_word_count": len(transcribed_words),
        "missing_words": sorted(original_set - transcribed_set)[:10],
        "extra_words":   sorted(transcribed_set - original_set)[:10],
    }


# ── Main pipeline ──────────────────────────────────────────────────────────

def main():
    text = (
        "Machine learning models learn patterns from data. "
        "They generalize from training examples to make predictions "
        "on new, unseen inputs. The quality of the training data "
        "directly determines the quality of the model's predictions."
    )

    print("\n=== HW2 Audio Pipeline ===")

    # ── Step 1/4: TTS – voice nova ─────────────────────────────────────
    try:
        tts_nova = text_to_speech(
            text, voice="nova",
            output_filename="voice_nova_sample.mp3",
            step_label="[1/4] Generating speech with voice: nova",
        )
    except Exception:
        print("  Pipeline aborted at step 1.")
        sys.exit(1)

    # ── Step 2/4: TTS – voice alloy ────────────────────────────────────
    try:
        tts_alloy = text_to_speech(
            text, voice="alloy",
            output_filename="voice_alloy_sample.mp3",
            step_label="[2/4] Generating speech with voice: alloy",
        )
    except Exception:
        print("  Pipeline aborted at step 2.")
        sys.exit(1)

    # ── Step 3/4: STT – transcribe nova output ─────────────────────────
    try:
        stt_result = speech_to_text(
            tts_nova["output_path"],
            step_label=f"[3/4] Transcribing {tts_nova['output_path']}",
        )
    except Exception:
        print("  Pipeline aborted at step 3.")
        sys.exit(1)

    # ── Step 4/4: Compare ───────────────────────────────────────────────
    comparison = compare_texts(text, stt_result["text"])
    print(f"\n[4/4] Comparing original vs transcribed text")
    print(f"  Original:    \"{text[:70]}...\"")
    print(f"  Transcribed: \"{stt_result['text'][:70]}...\"")
    print(f"  Word overlap accuracy: {comparison['word_overlap_accuracy']}%")
    if comparison["missing_words"]:
        print(f"  Missing words: {', '.join(comparison['missing_words'])}")
    if comparison["extra_words"]:
        print(f"  Extra words: {', '.join(comparison['extra_words'])}")

    # ── Cost and latency summary ────────────────────────────────────────
    avg_tts = round(_session["tts_total_latency"] / _session["tts_calls"], 2)
    avg_stt = round(_session["stt_total_latency"] / _session["stt_calls"], 2)
    total   = round(_session["tts_total_cost"] + _session["stt_total_cost"], 5)

    print(f"\n=== Cost and Latency Summary ===")
    print(f"  TTS calls:  {_session['tts_calls']} | "
          f"Total cost: ${_session['tts_total_cost']:.4f} | "
          f"Avg latency: {avg_tts}s")
    print(f"  STT calls:  {_session['stt_calls']} | "
          f"Total cost: ${_session['stt_total_cost']:.4f} | "
          f"Avg latency: {avg_stt}s")
    print(f"  Pipeline total: ${total}")
    print(f"\n  Cost log: {COST_LOG}")

    # Scale projection
    print(f"\n  If your product processes 100 passages/day:")
    print(f"    Daily cost:  ~${total * 100:.2f}")
    print(f"    Monthly:     ~${total * 100 * 30:.2f}")

    print(f"\n=== Pipeline complete ===\n")


if __name__ == "__main__":
    main()
