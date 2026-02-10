# Updated VADER Test Log

Source: `analysis.json` (all saved analyses)

Label rule: Positive if compound >= 0.05; Negative if compound <= -0.05; Neutral otherwise.

| # | Text entered | Expected | Predicted | Correct? |
|---:|---|---:|---|---:|
| 1 | ina mo ka | Negative | Neutral | No |
| 2 | I love this! | Positive | Positive | Yes |
| 3 | Wow! | Positive | Positive | Yes |
| 4 | So amazing! | Positive | Positive | Yes |
| 5 | bobo | Negative | Neutral | No |
| 6 | fuck you! | Negative | Negative | Yes |
| 7 | fuck your dad! | Negative | Negative | Yes |
| 8 | saksakin kita! | Negative | Neutral | No |
| 9 | motherfucker! | Negative | Negative | Yes |
|10 | shibal! | Negative | Neutral | No |
|11 | shit! | Negative | Negative | Yes |
|12 | love | Positive | Positive | Yes |
|13 | this cost an arm and a leg | Negative | Neutral | No |
|14 | I love this product, it's amazing! | Positive | Positive | Yes |
|15 | This is the worst service I have ever experienced. | Negative | Negative | Yes |
|16 | It is okay, nothing down special. | Neutral | Negative | No |
|17 | i wanna kil myself | Negative | Neutral | No |
|18 | i wanna kill myself | Negative | Negative | Yes |
|19 | i wanna kill my dog | Negative | Negative | Yes |
|20 | i wanna eat my dog | Negative | Neutral | No |
|21 | i wanna kill | Negative | Negative | Yes |
|22 | I'm so disappointed | Negative | Negative | Yes |
|23 | Meh | Neutral | Negative | No |
|24 | BEST PURCHASE EVER!!! | Positive | Positive | Yes |
|25 | This movie was sick (in a good way). | Positive | Negative | No |
|26 | Can't recommend this enough. | Positive | Negative | No |
|27 | The product arrived on time | Neutral | Neutral | Yes |
|28 | I absolutely love, love, love it!!! | Positive | Positive | Yes |
|29 | Absolutely fantastic! Exceeded my expectations. | Positive | Positive | Yes |
|30 | good boy | Positive | Positive | Yes |

Summary
- Total tests: 30
- Correct predictions: 19
- Incorrect predictions: 11
- Accuracy (%) = (19 / 30) × 100 = 63.33%

Observations
- VADER works well on clear positive or negative sentences like "I love this" or "This is the worst".
- Short words or single-word replies (e.g., "Meh", insults) are often wrong or labeled Neutral.
- Negations and phrases like "not unhappy" can be confusing and give mixed results.
- Sarcasm, slang, and local words often cause wrong labels.
- Some violent or suicidal lines need extra checks (safety handling).

Notes
- "Expected" labels are the human judgments before seeing VADER's output.
- I can add compound scores to the table or change the expected labels if you want.

Limitations and possible improvements

Limitations: VADER is a dictionary and rule tool. It misses meaning in hard cases like sarcasm, slang, mixed languages, or very short replies. It also does not give a calibrated confidence score or handle safety issues (violent or suicidal content) well.

Possible improvements: add simple text cleaning (fix spelling, normalize slang), extend the word list for local terms, and collect a small labeled set to train a simple classifier on top of VADER features. Also add a safety flag and let users change thresholds in the UI.

Reflection

- What Copilot GPT-5-Mini helped with: created the analyzer script, added JSON saving, built the Streamlit UI, and generated test logs and summaries.
- What I learned from its suggestions: VADER works well on clear text, fails on short/slang/sarcasm, and Streamlit is fast for prototyping dashboards.
- Why human understanding is still required: humans must set expected labels, handle nuance and safety cases, tune thresholds, and verify results before using them.
