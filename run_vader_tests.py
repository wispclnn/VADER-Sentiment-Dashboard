from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tests = [
    ("I love this product, it's amazing!", "Positive"),
    ("This is the worst service I have ever experienced.", "Negative"),
    ("It is okay, nothing special.", "Neutral"),
    ("Absolutely fantastic! Exceeded my expectations.", "Positive"),
    ("I hate it. Completely useless.", "Negative"),
    ("Not bad, could be better.", "Neutral"),
    ("I'm not happy with this.", "Negative"),
    ("I'm not unhappy with this.", "Neutral"),
    ("What a great day :)", "Positive"),
    ("Terrible, just terrible...", "Negative"),
    ("Meh.", "Neutral"),
    ("I absolutely love, love, love it!!!", "Positive"),
    ("I'm so disappointed :(", "Negative"),
    ("The product arrived on time.", "Neutral"),
    ("Can't recommend this enough.", "Positive"),
    ("Fine; works as advertised.", "Neutral"),
    ("Worst. Experience. Ever.", "Negative"),
    ("Could be worse.", "Neutral"),
    ("I guess it's fine.", "Neutral"),
    ("BEST PURCHASE EVER!!!", "Positive"),
    ("Oh great, another phone call. Just what I needed.", "Negative"),
    ("This movie was sick (in a good way).", "Positive"),
]

analyzer = SentimentIntensityAnalyzer()

print("TEXT|||EXPECTED|||COMPOUND|||PREDICTED")
for text, expected in tests:
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        predicted = 'Positive'
    elif compound <= -0.05:
        predicted = 'Negative'
    else:
        predicted = 'Neutral'
    # Escape pipe characters
    safe_text = text.replace('|', '\\|')
    print(f"{safe_text}|||{expected}|||{compound:.4f}|||{predicted}")
