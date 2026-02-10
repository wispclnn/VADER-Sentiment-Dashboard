"""
sentiment_baseline.py
Accepts text input, computes VADER sentiment (pos, neu, neg, compound), and prints the scores
and a final sentiment label using the rule:
  - Positive if compound >= 0.05
  - Negative if compound <= -0.05
  - Neutral otherwise

Usage examples:
  python sentiment_baseline.py -t "I love this product!"
  echo "This is ok." | python sentiment_baseline.py
  python sentiment_baseline.py  # will prompt for input

Requires the vaderSentiment package: pip install vaderSentiment
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import argparse
import sys
import json
import os
from datetime import datetime


def label_from_compound(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute VADER sentiment for input text.")
    parser.add_argument("-t", "--text", help="Text to analyze. If omitted, will read from stdin or prompt.")
    parser.add_argument("-o", "--output", help="Write result to JSON file (path). If omitted, no file is written.")
    args = parser.parse_args()

    if args.text:
        text = args.text.strip()
    else:
        # If there's piped input, read it
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            try:
                text = input("Enter text to analyze: ").strip()
            except EOFError:
                text = ""

    if not text:
        print("No text provided.", file=sys.stderr)
        sys.exit(1)

    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)

    # Print the sentiment scores
    print("Sentiment scores:")
    print(f"  pos:      {scores['pos']:.4f}")
    print(f"  neu:      {scores['neu']:.4f}")
    print(f"  neg:      {scores['neg']:.4f}")
    print(f"  compound: {scores['compound']:.4f}")

    # Determine and print final label
    label = label_from_compound(scores['compound'])
    print(f"Final sentiment: {label}")

    # Always save results to JSON. Use provided path or a single default filename (overwrite).
    result = {
        "text": text,
        "scores": {
            "pos": scores["pos"],
            "neu": scores["neu"],
            "neg": scores["neg"],
            "compound": scores["compound"]
        },
        "label": label
    }

    output_path = args.output if args.output else "analysis.json"
    # Ensure parent directory exists if a directory was provided
    parent = os.path.dirname(os.path.abspath(output_path))
    if parent and not os.path.exists(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception:
            pass

    # Read existing data if present and append the new result into a JSON array
    data = None
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            # If file can't be read or is malformed, we'll overwrite with a fresh list
            data = None

    if data is None:
        data_list = [result]
    elif isinstance(data, list):
        data_list = data
        data_list.append(result)
    elif isinstance(data, dict):
        # Convert single-object file into an array
        data_list = [data, result]
    else:
        # Unexpected content, replace with new list
        data_list = [result]

    try:
        with open(output_path, 'w', encoding='utf-8') as fh:
            json.dump(data_list, fh, ensure_ascii=False, indent=2)
        print(f"Saved analysis to {output_path} (total entries: {len(data_list)})")
    except Exception as e:
        print(f"Failed to write JSON file: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
