# Sentiment Baseline (VADER)

A small project that analyzes text sentiment using VADER and saves results to JSON. It includes a command-line analyzer and a simple Streamlit dashboard.

## Files
- `sentiment_baseline.py` - command-line analyzer, writes analyses to `analysis.json`.
- `streamlit_app.py` - Streamlit UI for entering text, viewing summary, and downloading data.
- `analysis.json` - stored analyses (array of entries).
- `run_vader_tests.py` - test runner used earlier.
- `test_log.md` - test cases and results.

## Requirements
- Python 3
- Install packages: `pip install vaderSentiment streamlit pandas plotly`

## How to run
- Command line analyzer:
  - `py sentiment_baseline.py -t "I love it"` (writes to `analysis.json`)
  - `echo "Meh" | py sentiment_baseline.py` (reads stdin)
- Streamlit UI:
  - `py -m streamlit run streamlit_app.py`

## Label rule
- Positive if compound >= 0.05
- Negative if compound <= -0.05
- Neutral otherwise

## Testing results (from saved analyses)
- Total tests: 30
- Correct predictions: 19
- Incorrect predictions: 11
- Accuracy: 63.33%

See `test_log.md` for detailed cases.

## Quick observations
- Works well on clear positive or negative sentences.
- Struggles with short replies, slang, sarcasm, and mixed languages.
- Negation and double negatives can be inconsistent.

## Limitations and possible improvements (short)
- Limitations: VADER is lexicon/rule based and misses nuance, sarcasm, slang, and non-English text. It has no confidence or safety handling.
- Improvements: add text cleaning, extend lexicon, collect labeled data and train a small classifier on top of VADER scores, add a safety flag and threshold controls in the UI.

## Prompt Engineering (short tips)
- Be specific: include desired format (JSON, table) and exact fields.
- Give examples: show one or two input/output examples.
- Ask for constraints: max length, language, thresholds.
- If you want code changes, point to filenames and desired behavior.

Example prompt:
- "Update `sentiment_baseline.py` to save results as an array in `analysis.json` and include a timestamp for each entry."

## AI Assistance Note
- This project used an AI assistant (GitHub Copilot) to generate scripts, UI, and test logs.
- The assistant helped with code, file edits, and documentation drafts.
- Human review was used to set expected labels, verify results, and make final decisions. Always review and test outputs before use.

---

If you want a production-grade API, a React UI, or improved models, I can scaffold next steps.
