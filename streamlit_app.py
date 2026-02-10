import streamlit as st
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import pandas as pd
import plotly.express as px

ANALYSIS_FILE = "analysis.json"

st.set_page_config(page_title="VADER Sentiment Dashboard", layout="wide")
st.title("VADER Sentiment Dashboard")

analyzer = SentimentIntensityAnalyzer()


def label_from_compound(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def load_data(path: str):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                return [data]
            if isinstance(data, list):
                return data
    except Exception:
        return []
    return []


def save_append(path: str, result: dict):
    data = load_data(path)
    data.append(result)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


# Left column: input and quick analyze
col1, col2 = st.columns([1, 2])
with col1:
    st.header("Analyze text")
    text_input = st.text_area("Enter text to analyze", height=150)
    if st.button("Analyze"):
        if not text_input.strip():
            st.error("Please enter some text.")
        else:
            scores = analyzer.polarity_scores(text_input)
            label = label_from_compound(scores["compound"])
            result = {
                "text": text_input,
                "scores": {
                    "pos": scores["pos"],
                    "neu": scores["neu"],
                    "neg": scores["neg"],
                    "compound": scores["compound"]
                },
                "label": label,
                "timestamp": datetime.utcnow().isoformat()
            }
            try:
                save_append(ANALYSIS_FILE, result)
                st.success(f"Saved analysis — label: {label}")
                st.json(result)
            except Exception as e:
                st.error(f"Failed to save analysis: {e}")

with col2:
    st.header("Summary")
    data = load_data(ANALYSIS_FILE)
    df = pd.json_normalize(data)
    if df.empty:
        st.info("No analyses yet. Analyze some text on the left.")
    else:
        st.metric("Total analyses", len(df))
        counts = df["label"].value_counts().to_dict()
        count_df = pd.DataFrame.from_dict(counts, orient="index", columns=["count"]).reset_index().rename(columns={"index":"label"})
        # Plotly bar chart so we can control bar thickness and colors
        color_map = {"Positive": "#2ca02c", "Negative": "#d62728", "Neutral": "#7f7f7f"}
        fig = px.bar(
            count_df,
            x="label",
            y="count",
            color="label",
            color_discrete_map=color_map,
            category_orders={"label": ["Positive", "Neutral", "Negative"]},
            height=260
        )
        # Make bars thinner by increasing gap and remove legend
        fig.update_layout(bargap=0.5, showlegend=False, xaxis_title=None, yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Recent analyses")
        show_df = df[["text", "label", "scores.compound"]].copy()
        show_df.columns = ["text", "label", "compound"]
        st.dataframe(show_df.sort_values(by="compound", ascending=False).reset_index(drop=True))

# Footer: Data & Export
if os.path.exists(ANALYSIS_FILE):
    with open(ANALYSIS_FILE, "r", encoding="utf-8") as fh:
        raw = fh.read()
    st.markdown("---")
    st.subheader("Data & Export")
    st.download_button("Download JSON", raw, file_name="analysis.json", mime="application/json")
    try:
        df_all = pd.json_normalize(load_data(ANALYSIS_FILE))
        st.download_button("Download CSV", df_all.to_csv(index=False).encode("utf-8"), file_name="analysis.csv", mime="text/csv")
    except Exception:
        pass
else:
    st.info("No analysis.json found yet.")

st.markdown("---")
st.caption("Built with Streamlit and VADER. Run: pip install streamlit vaderSentiment pandas\nthen: streamlit run streamlit_app.py")
