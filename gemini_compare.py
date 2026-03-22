
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit(
        "ERROR: GEMINI_API_KEY not found. "
        "Make sure you have a .env file with GEMINI_API_KEY=your-key-here"
    )

client = genai.Client(api_key=api_key)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

PROMPT = (
    "A farmer has a fox, a chicken, and a bag of grain. "
    "He needs to cross a river in a boat that can only carry him and one item at a time. "
    "If left alone, the fox will eat the chicken, and the chicken will eat the grain. "
    "How can the farmer get everything across safely? Explain step by step."
)

PRICING = {
    "gemini-2.5-flash": {
        "input_per_token": 0.30 / 1_000_000,    # $0.30 per 1M input tokens
        "output_per_token": 2.50 / 1_000_000,    # $2.50 per 1M output tokens
    },
    "gemini-2.5-flash-lite": {
        "input_per_token": 0.10 / 1_000_000,    # $0.10 per 1M input tokens
        "output_per_token": 0.40 / 1_000_000,   # $0.40 per 1M output tokens
    },
}

MAX_RETRIES = 3


def call_model(model_name: str, prompt: str) -> dict:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            start = time.perf_counter()
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            usage = response.usage_metadata
            input_tokens = usage.prompt_token_count
            output_tokens = usage.candidates_token_count
            total_tokens = usage.total_token_count

            prices = PRICING.get(model_name, PRICING["gemini-2.5-flash"])
            cost = (
                input_tokens * prices["input_per_token"]
                + output_tokens * prices["output_per_token"]
            )

            return {
                "model": model_name,
                "response_text": response.text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "latency_ms": round(elapsed_ms),
                "cost_usd": cost,
            }

        except errors.ClientError as e:
            if "429" in str(e) and attempt < MAX_RETRIES:
                wait = 60 * attempt
                print(f"   Rate limited. Waiting {wait}s before retry {attempt + 1}/{MAX_RETRIES}...")
                time.sleep(wait)
            else:
                raise


print("=" * 70)
print("HW1 — Gemini Model Comparison")
print("=" * 70)
print(f"\nPrompt:\n  {PROMPT}\n")

results = []
for model in MODELS:
    print(f"{'─' * 70}")
    print(f"Calling {model} …")
    result = call_model(model, PROMPT)
    results.append(result)

    print(f"\n  Response from {model}:\n")
    print(result["response_text"])
    print(f"\n  Token usage:")
    print(f"    Input tokens:  {result['input_tokens']}")
    print(f"    Output tokens: {result['output_tokens']}")
    print(f"    Total tokens:  {result['total_tokens']}")
    print(f"    Latency:       {result['latency_ms']} ms")
    print(f"    Cost (paid):   ${result['cost_usd']:.6f}")
    print()

print("=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
header = f"{'Call':<6}{'Model':<32}{'In':>6}{'Out':>7}{'Total':>7}{'Latency':>10}{'Cost':>12}"
print(header)
print("-" * len(header))
for i, r in enumerate(results, start=1):
    print(
        f"{i:<6}"
        f"{r['model']:<32}"
        f"{r['input_tokens']:>6}"
        f"{r['output_tokens']:>7}"
        f"{r['total_tokens']:>7}"
        f"{r['latency_ms']:>8} ms"
        f"  ${r['cost_usd']:.6f}"
    )
print()