import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="VoxPop Brand Intelligence",
    layout="wide"
)

st.title("🚨 VoxPop: Brand Sentiment Intelligence Dashboard")
st.markdown("Real-time brand crisis monitoring and sentiment analytics")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sample_reviews.csv")  # change if needed
    return df

df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment",
    options=df['sentiment'].unique(),
    default=df['sentiment'].unique()
)

filtered_df = df[df['sentiment'].isin(sentiment_filter)]

# -------------------------------
# KPI METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(filtered_df))
col2.metric("Unique Users", filtered_df['user'].nunique())
col3.metric("Avg Anger Score", round(filtered_df.get('anger_score', pd.Series([0])).mean(), 3))

st.divider()

# -------------------------------
# DONUT CHART — SENTIMENT
# -------------------------------
st.subheader("🧭 Sentiment Distribution")

sent_counts = filtered_df['sentiment'].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(sent_counts.values, labels=sent_counts.index, autopct='%1.1f%%')
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig1.gca().add_artist(centre_circle)
ax1.axis('equal')

st.pyplot(fig1)

# -------------------------------
# WORD CLOUD
# -------------------------------
st.subheader("☁️ Negative Review Word Cloud")

neg_text = " ".join(
    filtered_df[filtered_df['sentiment'] == 0]['clean_text'].dropna().astype(str)
)

if neg_text.strip():
    wc = WordCloud(width=800, height=400, background_color='white').generate(neg_text)

    fig2, ax2 = plt.subplots()
    ax2.imshow(wc)
    ax2.axis("off")
    st.pyplot(fig2)
else:
    st.info("No negative text available.")

# -------------------------------
# SENTIMENT OVER TIME
# -------------------------------
st.subheader("📈 Sentiment Trend Over Time")

if 'date' in filtered_df.columns:
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')
    trend = filtered_df.groupby(filtered_df['date'].dt.date)['sentiment'].mean()

    fig3, ax3 = plt.subplots()
    trend.plot(ax=ax3)
    ax3.set_ylabel("Average Sentiment")
    ax3.set_xlabel("Date")

    st.pyplot(fig3)

# -------------------------------
# TOP COMPLAINTS (SMART TOUCH ⭐)
# -------------------------------
st.subheader("🔥 Top Complaint Keywords")

if 'clean_text' in filtered_df.columns:
    words = (
        filtered_df['clean_text']
        .dropna()
        .str.split()
        .explode()
        .value_counts()
        .head(10)
    )
    st.bar_chart(words)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Built by Ramya | VoxPop AI")