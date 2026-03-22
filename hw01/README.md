# HW1 — Gemini Model Comparison

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026

## What This Project Does

This script sends the same logic puzzle (the classic fox-chicken-grain river crossing problem) to two different Google Gemini models and compares their responses. It measures token usage, latency, and calculates the paid-tier cost equivalent for each call.

### How to Run

1. **Clone this repository** and navigate to the `hw01/` folder.
2. **Create a `.env` file** by copying the example:
   ```bash
   cp .env.example .env
   ```
3. **Add your Gemini API key** to `.env`:
   ```
   GEMINI_API_KEY=AIza...your-real-key-here
   ```
4. **Install dependencies** (using uv or pip):
   ```bash
   uv pip install python-dotenv google-genai
   # or
   pip install python-dotenv google-genai
   ```
5. **Run the script:**
   ```bash
   python gemini_compare.py
   ```

### Models Used

| Model                    | Description                                    |
| ------------------------ | ---------------------------------------------- |
| `gemini-2.5-flash`       | Balanced model — good capability and speed     |
| `gemini-2.5-flash-lite`  | Lightweight variant — faster and cheaper        |

---

## Cost Analysis

| Call | Model                  | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Cost (paid equiv.) |
| ---- | ---------------------- | ------------ | ------------- | ------------ | ------------- | ------------------- |
| 1    | gemini-2.5-flash       | 70           | 687           | 2,399        | 9,863         | $0.001739           |
| 2    | gemini-2.5-flash-lite  | 70           | 624           | 694          | 1,843         | $0.000257           |

---

## Reflection (5 Sentences)

1. Gemini-2.5-flash-lite was significantly faster at around 2 seconds compared to gemini-2.5-flash which took almost 10 seconds, so the speed difference was much bigger than I expected.
2. Both models solved the river crossing puzzle correctly in exactly 7 steps, so the quality of the answers was essentially the same despite the speed and cost differences.
3. The total token count for flash was 2,399 which was much higher than its actual input plus output of 757, meaning the model uses hidden thinking tokens that are not shown in the response.
4. The cost difference was dramatic flash was roughly 7 times more expensive than flash-lite ($0.0017 vs $0.0003), which really adds up if you are making thousands of API calls.
5. This showed me that a lighter model can produce equally correct and well-structured answers for straightforward reasoning tasks, so picking the most powerful model is not always necessary.
I wrote it myself but grammar i fixed with AI .... its mine
---

