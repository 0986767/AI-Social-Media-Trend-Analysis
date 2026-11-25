
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import re

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Social Media Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PROFESSIONAL CSS DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080f20, #111b35, #17132e);
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111c35, #201638);
    border-right: 1px solid #39466b;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label, span {
    color: #d5def0;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #192b4a, #292044);
    border: 1px solid #53658e;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #a5b4fc !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #46577d;
    border-radius: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    padding: 10px 20px;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7e22ce);
    color: white;
    border: 1px solid #a78bfa;
}

[data-testid="stFileUploader"] {
    background: #182744;
    border: 1px dashed #818cf8;
    border-radius: 15px;
    padding: 15px;
}

hr {
    border-color: #39466b;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA LOADING
# ==========================================

BASE_DIR = Path(__file__).resolve().parent


def load_csv(filename):
    path = BASE_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return None


metrics_df = load_csv("dashboard_metrics.csv")
saved_topic_df = load_csv("final_trending_topics_analysis.csv")
saved_sentiment_df = load_csv("cleaned_sentiment_data.csv")


# ==========================================
# TOPIC IDENTIFICATION
# ==========================================

topic_keywords = {
    "Technology": [
        "technology", "ai", "software", "computer",
        "mobile", "digital", "robot"
    ],
    "Fitness": [
        "fitness", "gym", "workout", "exercise", "health"
    ],
    "Travel": [
        "travel", "trip", "beach", "mountain", "explore"
    ],
    "Food": [
        "food", "recipe", "cooking", "restaurant", "pizza"
    ],
    "Education": [
        "education", "study", "student", "college", "learning"
    ],
    "Sports": [
        "sports", "cricket", "football", "match", "player"
    ],
    "Nature": [
        "nature", "park", "tree", "forest", "environment"
    ],
    "Entertainment": [
        "movie", "music", "film", "actor", "entertainment"
    ],
    "Lifestyle": [
        "lifestyle", "fashion", "style", "daily"
    ],
    "Business": [
        "business", "market", "company", "startup"
    ]
}


def identify_topic(text):
    text = str(text).lower()

    for topic, keywords in topic_keywords.items():
        for word in keywords:
            if re.search(r"\b" + re.escape(word) + r"\b", text):
                return topic

    return "Other"


# ==========================================
# SESSION STATE
# ==========================================

if "uploaded_posts" not in st.session_state:
    st.session_state.uploaded_posts = None

if "uploaded_topics" not in st.session_state:
    st.session_state.uploaded_topics = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("# 📊 AI ANALYTICS")
st.sidebar.caption("SOCIAL MEDIA TREND ANALYSIS")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard Overview",
        "📁 Dataset Upload",
        "🏆 Topic Analysis",
        "😊 Sentiment Analysis",
        "#️⃣ Hashtag Analysis"
    ],
    key="navigation"
)

st.sidebar.divider()

st.sidebar.markdown("### 🚀 Project Features")
st.sidebar.caption("✔ Dataset Processing")
st.sidebar.caption("✔ Trend Identification")
st.sidebar.caption("✔ Sentiment Analysis")
st.sidebar.caption("✔ Engagement Analysis")
st.sidebar.caption("✔ Interactive Visualizations")

st.sidebar.divider()
st.sidebar.caption("Powered by Python | NLP | Machine Learning")


# ==========================================
# HEADER
# ==========================================

st.markdown("""
# 📊 AI-Based Social Media Trend Analysis

### Discover • Analyze • Predict • Visualize

An intelligent dashboard for analyzing social media trends,
sentiment and audience engagement.
""")

st.divider()


# ==========================================
# MAIN PROJECT DATA
# IMPORTANT: Always use existing project dataset.
# Uploaded dataset will NOT affect this section.
# ==========================================

posts_df = (
    saved_sentiment_df.copy()
    if saved_sentiment_df is not None
    else None
)

topic_df = (
    saved_topic_df.copy()
    if saved_topic_df is not None
    else None
)

data_source = "Existing Project Dataset"


# ==========================================
# DASHBOARD OVERVIEW
# ==========================================

if page == "🏠 Dashboard Overview":

    st.subheader("✨ System Overview")

    st.caption(f"Current Data Source: {data_source}")

    total_posts = len(posts_df) if posts_df is not None else 0

    accuracy = 0

    if metrics_df is not None and not metrics_df.empty:
        if "Model_Accuracy" in metrics_df.columns:
            accuracy = float(metrics_df.loc[0, "Model_Accuracy"])

    top_topic = "N/A"
    trend_score = 0

    if topic_df is not None and not topic_df.empty:
        if "Trend_Score" in topic_df.columns:
            winner = topic_df.sort_values(
                "Trend_Score", ascending=False
            ).iloc[0]

            top_topic = winner["Topic"]
            trend_score = float(winner["Trend_Score"])

    a, b, c, d = st.columns(4)

    a.metric("📌 Total Posts", f"{total_posts:,}")
    b.metric("🎯 Model Accuracy", f"{accuracy:.2f}%")
    c.metric("🔥 Top Trending Topic", str(top_topic))
    d.metric("📈 Trend Score", f"{trend_score:.2f}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown("### 🏆 Trending Topics")

        if topic_df is not None and not topic_df.empty:

            fig = px.bar(
                topic_df.head(10),
                x="Topic",
                y="Trend_Score",
                color="Trend_Score",
                text_auto=".1f",
                color_continuous_scale="Turbo",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-35
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No existing topic data available.")

    with right:
        st.markdown("### 😊 Sentiment Distribution")

        if posts_df is not None and "Sentiment" in posts_df.columns:

            counts = (
                posts_df["Sentiment"]
                .astype(str)
                .str.strip()
                .str.capitalize()
                .value_counts()
                .reset_index()
            )

            counts.columns = ["Sentiment", "Count"]

            fig = px.pie(
                counts,
                names="Sentiment",
                values="Count",
                hole=0.55,
                color="Sentiment",
                color_discrete_map={
                    "Positive": "#22c55e",
                    "Negative": "#ef4444",
                    "Neutral": "#eab308"
                },
                template="plotly_dark"
            )

            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Sentiment column is not available.")

    st.divider()

    st.markdown("### 💡 About This System")

    x, y, z = st.columns(3)

    with x:
        with st.container(border=True):
            st.markdown("### 🧠 AI Analysis")
            st.write("Analyze social media content and identify topics.")

    with y:
        with st.container(border=True):
            st.markdown("### 📊 Data Visualization")
            st.write("Understand trends through interactive charts.")

    with z:
        with st.container(border=True):
            st.markdown("### 🚀 Trend Discovery")
            st.write("Discover popular topics using engagement scores.")


# ==========================================
# DATASET UPLOAD
# ==========================================

elif page == "📁 Dataset Upload":

    st.subheader("📁 Upload Your Social Media Dataset")

    st.write(
        "Upload a CSV file containing social media posts "
        "to perform independent trend analysis."
    )

    uploaded_file = st.file_uploader(
        "Choose CSV Dataset",
        type=["csv"],
        key="dataset_uploader"
    )

    if uploaded_file is not None:

        try:
            uploaded_file.seek(0)
            raw_df = pd.read_csv(uploaded_file)

            # Clear previous results when a different file is selected
            if st.session_state.uploaded_filename != uploaded_file.name:

                st.session_state.uploaded_posts = None
                st.session_state.uploaded_topics = None
                st.session_state.uploaded_filename = uploaded_file.name

            st.success("Dataset uploaded successfully!")

            # DATASET PREVIEW
            st.markdown("### 👀 Dataset Preview")

            st.dataframe(
                raw_df.head(10),
                use_container_width=True,
                hide_index=True
            )

            # DATASET INFORMATION
            st.markdown("### 📋 Dataset Information")

            p1, p2, p3 = st.columns(3)

            p1.metric("Total Rows", len(raw_df))
            p2.metric("Total Columns", len(raw_df.columns))
            p3.metric(
                "Missing Values",
                int(raw_df.isnull().sum().sum())
            )

            st.write(
                "Available Columns:",
                ", ".join(raw_df.columns)
            )

            st.divider()

            # ANALYZE BUTTON
            if st.button(
                "🚀 Analyze Uploaded Dataset",
                use_container_width=True
            ):

                if "Text" not in raw_df.columns:

                    st.error(
                        "Dataset must contain a 'Text' column."
                    )

                else:

                    df = raw_df.copy()

                    df["Text"] = (
                        df["Text"]
                        .fillna("")
                        .astype(str)
                    )

                    # Engagement columns
                    for col in ["Likes", "Comments", "Retweets"]:

                        if col not in df.columns:
                            df[col] = 0

                        df[col] = pd.to_numeric(
                            df[col],
                            errors="coerce"
                        ).fillna(0)

                    # Topic identification
                    df["Topic"] = df["Text"].apply(
                        identify_topic
                    )

                    # Engagement calculation
                    df["Engagement"] = (
                        df["Likes"]
                        + df["Comments"]
                        + df["Retweets"]
                    )

                    # Topic-wise analysis
                    topic_analysis = df.groupby("Topic").agg(
                        Frequency=("Text", "count"),
                        Total_Likes=("Likes", "sum"),
                        Total_Comments=("Comments", "sum"),
                        Total_Retweets=("Retweets", "sum"),
                        Total_Engagement=("Engagement", "sum")
                    ).reset_index()

                    max_frequency = topic_analysis["Frequency"].max()
                    max_engagement = topic_analysis["Total_Engagement"].max()

                    if max_frequency > 0:
                        topic_analysis["Frequency_Score"] = (
                            topic_analysis["Frequency"]
                            / max_frequency * 100
                        )
                    else:
                        topic_analysis["Frequency_Score"] = 0

                    if max_engagement > 0:
                        topic_analysis["Engagement_Score"] = (
                            topic_analysis["Total_Engagement"]
                            / max_engagement * 100
                        )
                    else:
                        topic_analysis["Engagement_Score"] = 0

                    # Trend Score
                    topic_analysis["Trend_Score"] = (
                        0.50 * topic_analysis["Frequency_Score"]
                        + 0.50 * topic_analysis["Engagement_Score"]
                    )

                    topic_analysis = topic_analysis.sort_values(
                        "Trend_Score",
                        ascending=False
                    ).reset_index(drop=True)

                    topic_analysis.insert(
                        0,
                        "Rank",
                        range(1, len(topic_analysis) + 1)
                    )

                    # Save only in uploaded dataset session state
                    st.session_state.uploaded_posts = df
                    st.session_state.uploaded_topics = topic_analysis
                    st.session_state.uploaded_filename = uploaded_file.name

                    st.success(
                        "Dataset analysis completed successfully!"
                    )

                    st.balloons()

            # ==========================================
            # DISPLAY UPLOADED DATASET RESULTS
            # These results appear ONLY on this page.
            # ==========================================

            if st.session_state.uploaded_posts is not None:

                if st.session_state.uploaded_filename == uploaded_file.name:

                    uploaded_posts = st.session_state.uploaded_posts
                    uploaded_topics = st.session_state.uploaded_topics

                    st.divider()

                    st.markdown("## 📊 Uploaded Dataset Analysis")

                    # POST ANALYSIS
                    st.markdown("### 📝 Post Analysis")

                    q1, q2, q3 = st.columns(3)

                    q1.metric(
                        "Total Posts",
                        len(uploaded_posts)
                    )

                    q2.metric(
                        "Total Topics",
                        uploaded_topics["Topic"].nunique()
                    )

                    q3.metric(
                        "Total Engagement",
                        int(uploaded_posts["Engagement"].sum())
                    )

                    st.dataframe(
                        uploaded_posts,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.divider()

                    # TRENDING TOPICS BELOW POST ANALYSIS
                    st.markdown("## 🔥 Trending Topics in Uploaded Dataset")

                    top_row = uploaded_topics.iloc[0]

                    r1, r2, r3 = st.columns(3)

                    r1.metric(
                        "🏆 Top Trending Topic",
                        str(top_row["Topic"])
                    )

                    r2.metric(
                        "📈 Trend Score",
                        f"{top_row['Trend_Score']:.2f}"
                    )

                    r3.metric(
                        "📌 Topic Frequency",
                        int(top_row["Frequency"])
                    )

                    # TRENDING TOPICS GRAPH
                    st.markdown("### 📊 Topic-wise Trend Score")

                    fig = px.bar(
                        uploaded_topics,
                        x="Topic",
                        y="Trend_Score",
                        color="Trend_Score",
                        text_auto=".1f",
                        color_continuous_scale="Turbo",
                        template="plotly_dark",
                        hover_data=[
                            "Frequency",
                            "Total_Engagement",
                            "Total_Likes",
                            "Total_Comments",
                            "Total_Retweets"
                        ]
                    )

                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis_tickangle=-35,
                        title="Trending Topics from Uploaded Dataset"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    # TOPIC RANKING TABLE
                    st.markdown("### 🏆 Trending Topics Ranking")

                    st.dataframe(
                        uploaded_topics,
                        use_container_width=True,
                        hide_index=True
                    )

                    # DOWNLOAD BUTTONS
                    st.download_button(
                        "⬇️ Download Trending Topics Analysis",
                        data=uploaded_topics.to_csv(
                            index=False
                        ).encode("utf-8"),
                        file_name="uploaded_trending_topics.csv",
                        mime="text/csv"
                    )

                    st.download_button(
                        "⬇️ Download Post Analysis",
                        data=uploaded_posts.to_csv(
                            index=False
                        ).encode("utf-8"),
                        file_name="uploaded_post_analysis.csv",
                        mime="text/csv"
                    )

        except Exception as e:

            st.error(f"Unable to read dataset: {e}")

    else:

        st.info("Please upload a CSV file to start analysis.")


# ==========================================
# TOPIC ANALYSIS
# Uses ONLY existing project dataset
# ==========================================

elif page == "🏆 Topic Analysis":

    st.subheader("🏆 Topic-wise Trend Analysis")

    if topic_df is not None and not topic_df.empty:

        st.caption("Analysis Source: Existing Project Dataset")

        fig = px.bar(
            topic_df,
            x="Topic",
            y="Trend_Score",
            color="Trend_Score",
            text_auto=".1f",
            color_continuous_scale="Turbo",
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_tickangle=-40
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("### 📋 Topic Analysis Records")

        st.dataframe(
            topic_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Topic Analysis",
            data=topic_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="topic_analysis.csv",
            mime="text/csv"
        )

    else:

        st.warning("No topic analysis data available.")


# ==========================================
# SENTIMENT ANALYSIS
# Uses ONLY existing project dataset
# ==========================================

elif page == "😊 Sentiment Analysis":

    st.subheader("😊 Sentiment Analysis")

    if posts_df is not None and "Sentiment" in posts_df.columns:

        sentiment_counts = (
            posts_df["Sentiment"]
            .astype(str)
            .str.strip()
            .str.capitalize()
            .value_counts()
            .reindex(
                ["Positive", "Negative", "Neutral"],
                fill_value=0
            )
            .reset_index()
        )

        sentiment_counts.columns = [
            "Sentiment",
            "Count"
        ]

        a, b, c = st.columns(3)

        a.metric(
            "😊 Positive",
            int(sentiment_counts.iloc[0]["Count"])
        )

        b.metric(
            "😞 Negative",
            int(sentiment_counts.iloc[1]["Count"])
        )

        c.metric(
            "😐 Neutral",
            int(sentiment_counts.iloc[2]["Count"])
        )

        fig = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            hole=0.5,
            color="Sentiment",
            color_discrete_map={
                "Positive": "#22c55e",
                "Negative": "#ef4444",
                "Neutral": "#eab308"
            },
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            sentiment_counts,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Sentiment column is not available in the existing dataset."
        )


# ==========================================
# HASHTAG ANALYSIS
# Uses ONLY existing project dataset
# ==========================================

elif page == "#️⃣ Hashtag Analysis":

    st.subheader("#️⃣ Hashtag Engagement Analysis")

    if posts_df is not None:

        hashtags = []

        if "Hashtags" in posts_df.columns:

            for value in posts_df["Hashtags"].dropna():

                hashtags.extend(
                    re.findall(
                        r"#?\w+",
                        str(value).lower()
                    )
                )

        elif "Text" in posts_df.columns:

            for value in posts_df["Text"].dropna():

                hashtags.extend(
                    re.findall(
                        r"#\w+",
                        str(value).lower()
                    )
                )

        hashtags = [
            tag.lstrip("#")
            for tag in hashtags
            if tag.strip("#")
        ]

        if hashtags:

            hashtag_df = pd.DataFrame({
                "Hashtag": hashtags
            })

            hashtag_counts = (
                hashtag_df["Hashtag"]
                .value_counts()
                .head(15)
                .reset_index()
            )

            hashtag_counts.columns = [
                "Hashtag",
                "Frequency"
            ]

            fig = px.bar(
                hashtag_counts,
                x="Hashtag",
                y="Frequency",
                color="Frequency",
                text="Frequency",
                color_continuous_scale="Plasma",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-35
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                hashtag_counts,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download Hashtag Analysis",
                data=hashtag_counts.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="hashtag_analysis.csv",
                mime="text/csv"
            )

        else:

            st.info("No hashtags found in the existing dataset.")

    else:

        st.warning("No existing project dataset available.")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    "<center>✨ AI-Based Social Media Trend Analysis System "
    "| Python | Streamlit | NLP | Machine Learning ✨</center>",
    unsafe_allow_html=True
)
