import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VoxPop AI Brand Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS (COLORFUL UI) ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
h1, h2, h3 {
    color: #ffffff;
}
.metric-box {
    background-color: #ffffff20;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA (ERROR SAFE) ----------------
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "voxpop_AI Brand sentiment.csv")

    if not os.path.exists(file_path):
        st.error(f"❌ File not found: {file_path}")
        st.stop()

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🔍 Filters")

year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df['year'].dropna().unique()),
    default=sorted(df['year'].dropna().unique())
)

sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    sorted(df['sentiment'].dropna().unique()),
    default=sorted(df['sentiment'].dropna().unique())
)

filtered_df = df[
    (df['year'].isin(year_filter)) &
    (df['sentiment'].isin(sentiment_filter))
]

# ---------------- TITLE ----------------
st.title("📊 VoxPop AI Brand Sentiment Dashboard")
st.markdown("### 🚀 Real-Time Brand Intelligence")

# ---------------- KPI ROW ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reviews", len(filtered_df))
col2.metric("Unique Users", filtered_df['username'].nunique())
col3.metric("Avg Anger Score", round(filtered_df['anger_score'].mean(), 3))
col4.metric("Topics Found", filtered_df['topic_cluster'].nunique())

# ---------------- SENTIMENT CHART ----------------
st.subheader("📈 Sentiment Distribution")

sent_counts = filtered_df['sentiment'].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(sent_counts.index.astype(str), sent_counts.values)
ax1.set_xlabel("Sentiment")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# ---------------- TOP TOPICS ----------------
st.subheader("🔥 Top Topic Clusters")

topic_counts = filtered_df['topic_cluster'].value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(topic_counts.index.astype(str), topic_counts.values)
ax2.invert_yaxis()
st.pyplot(fig2)

# ---------------- WORD CLOUD ----------------
st.subheader("☁️ Negative Reviews WordCloud")

text_column = "clean_text" if "clean_text" in filtered_df.columns else "text"

neg_text = filtered_df[filtered_df['sentiment'] == 0][text_column].dropna().astype(str)

if len(neg_text) > 0:
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black"
    ).generate(" ".join(neg_text))

    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.warning("No negative reviews available for wordcloud.")

# ---------------- RECENT REVIEWS ----------------
st.subheader("📝 Recent Reviews")

display_cols = ['username', 'sentiment', 'anger_score', text_column]
display_cols = [c for c in display_cols if c in filtered_df.columns]

st.dataframe(filtered_df[display_cols].head(50), use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Built with Ramya | VoxPop AI Intelligence")
