import streamlit as st

from news_api import fetch_news
from gnews_api import fetch_gnews
from open_meteo_api import fetch_weather
from retrieval import retrieve_articles
from ai import generate_intelligence


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide"
)


# ==================================================
# CUSTOM DESIGN
# ==================================================

st.markdown(
    """
    <style>

    /* ---------- Main background ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(37, 99, 235, 0.10),
                transparent 35%
            ),
            radial-gradient(
                circle at top left,
                rgba(14, 165, 233, 0.06),
                transparent 30%
            );
    }


    /* ---------- Main content ---------- */

    .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }


    /* ---------- Header ---------- */

    .rtip-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.5rem;

        border: 1px solid rgba(59, 130, 246, 0.20);
        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.78)
            );

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.20);
    }


    .rtip-title {
        font-size: 1.55rem;
        font-weight: 750;
        color: #f8fafc;
        letter-spacing: -0.02em;
        margin: 0;
    }


    .rtip-subtitle {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 0.25rem;
    }


    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        padding: 6px 11px;

        border-radius: 999px;

        background: rgba(34, 197, 94, 0.10);
        border: 1px solid rgba(34, 197, 94, 0.25);

        color: #4ade80;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
    }


    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 10px rgba(74, 222, 128, 0.8);
    }


    /* ---------- Welcome area ---------- */

    .welcome-box {
        text-align: center;
        padding: 2.4rem 1rem 2rem;
    }


    .welcome-icon {
        font-size: 2.7rem;
        margin-bottom: 0.4rem;
    }


    .welcome-title {
        font-size: 1.65rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.35rem;
    }


    .welcome-text {
        color: #94a3b8;
        font-size: 0.95rem;
    }


    /* ---------- Section labels ---------- */

    .section-label {
        font-size: 0.70rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        color: #64748b;
        margin-bottom: 0.7rem;
    }


    /* ---------- Chat input ---------- */

    div[data-testid="stChatInput"] {
        border-radius: 16px;
    }


    div[data-testid="stChatInput"] textarea {
        border-radius: 14px;
    }


    /* ---------- Assistant message ---------- */

    div[data-testid="stChatMessage"] {
        border-radius: 16px;
    }


    /* ---------- Intelligence heading ---------- */

    .intelligence-heading {
        padding: 0.85rem 1rem;

        border-left: 3px solid #3b82f6;

        background: rgba(37, 99, 235, 0.07);

        border-radius: 8px;

        color: #dbeafe;

        font-weight: 700;

        margin-bottom: 1rem;
    }


    /* ---------- Source cards ---------- */

    .source-card {
        padding: 1rem 1.1rem;
        margin: 0.7rem 0;

        border: 1px solid rgba(148, 163, 184, 0.14);

        border-radius: 13px;

        background: rgba(15, 23, 42, 0.55);

        transition: 0.2s ease;
    }


    .source-card:hover {
        border-color: rgba(59, 130, 246, 0.35);

        background: rgba(30, 41, 59, 0.75);
    }


    .source-title {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.94rem;
    }


    .source-meta {
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 0.35rem;
    }


    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a,
                #111827
            );
    }


    section[data-testid="stSidebar"] * {
        color: #cbd5e1;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.18);
        background: rgba(30, 41, 59, 0.55);
        transition: 0.2s ease;
    }


    .stButton > button:hover {
        border-color: rgba(59, 130, 246, 0.55);
        background: rgba(37, 99, 235, 0.12);
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="rtip-header">

        <div>
            <div class="rtip-title">
                🛰️ Real-Time Intelligence Platform
            </div>

            <div class="rtip-subtitle">
                Ask questions about current events and get
                AI-powered intelligence based on recent news.
            </div>
        </div>

        <div class="live-badge">
            <span class="live-dot"></span>
            LIVE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## RTIP")

    st.caption("INTELLIGENCE CONFIGURATION")

    st.markdown("### News Sources")

    st.checkbox(
        "NewsData.io",
        value=True,
        disabled=True
    )

    st.checkbox(
        "GNews",
        value=True,
        disabled=True
    )

    st.markdown("### Intelligence")

    st.checkbox(
        "Source comparison",
        value=True,
        disabled=True
    )

    st.checkbox(
        "Conflict detection",
        value=True,
        disabled=True
    )

    st.divider()

    st.caption(
        "Real-Time Intelligence Platform"
    )


# ==================================================
# WELCOME SCREEN
# ==================================================

if "messages" not in st.session_state:

    st.markdown(
        """
        <div class="welcome-box">

            <div class="welcome-icon">
                🛰️
            </div>

            <div class="welcome-title">
                What is happening right now?
            </div>

            <div class="welcome-text">
                Ask about world events, politics, technology,
                conflicts, or breaking news.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input(
    "Ask about current events..."
)


# ==================================================
# PROCESS QUESTION
# ==================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # ------------------------------------------------
    # Detect question type
    # ------------------------------------------------

    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "wind",
        "humidity"
    ]

    is_weather_question = any(
        keyword in question.lower()
        for keyword in weather_keywords
    )


    # =================================================
    # WEATHER
    # =================================================

    if is_weather_question:

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Getting current weather..."
                ):

                    weather = fetch_weather(
                        latitude=33.6844,
                        longitude=73.0479
                    )

                current = weather["current"]

                st.markdown(
                    '<div class="intelligence-heading">'
                    'CURRENT WEATHER'
                    '</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Temperature",
                        f"{current['temperature_2m']} °C"
                    )

                with col2:
                    st.metric(
                        "Humidity",
                        f"{current['relative_humidity_2m']}%"
                    )

                with col3:
                    st.metric(
                        "Wind",
                        f"{current['wind_speed_10m']} km/h"
                    )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(e)


    # =================================================
    # NEWS
    # =================================================

    else:

        with st.chat_message("assistant"):

            try:

                # -------------------------------------
                # Fetch News
                # -------------------------------------

                with st.spinner(
                    "Searching current news..."
                ):

                    newsdata_articles = fetch_news(
                        query=question,
                        language="en",
                        limit=15
                    )

                    gnews_articles = fetch_gnews(
                        query=question,
                        language="en",
                        max_results=10
                    )

                    articles = (
                        newsdata_articles
                        + gnews_articles
                    )


                # -------------------------------------
                # Check Articles
                # -------------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # -------------------------------------
                # Retrieve
                # -------------------------------------

                with st.spinner(
                    "Finding the most relevant information..."
                ):

                    relevant_articles = retrieve_articles(
                        articles,
                        question,
                        max_articles=8
                    )


                if not relevant_articles:

                    st.warning(
                        "No relevant articles were found."
                    )

                    st.stop()


                # -------------------------------------
                # AI Analysis
                # -------------------------------------

                with st.spinner(
                    "Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # -------------------------------------
                # Intelligence Brief
                # -------------------------------------

                st.markdown(
                    '<div class="intelligence-heading">'
                    'INTELLIGENCE BRIEF'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(answer)


                # -------------------------------------
                # Sources
                # -------------------------------------

                st.divider()

                st.markdown(
                    '<div class="section-label">'
                    'SOURCES'
                    '</div>',
                    unsafe_allow_html=True
                )


                for article in relevant_articles:

                    title = article.get(
                        "title",
                        "Untitled"
                    )

                    source = article.get(
                        "source",
                        "Unknown source"
                    )

                    url = article.get("url")

                    published = article.get(
                        "published",
                        "Unknown date"
                    )


                    st.markdown(
                        f"""
                        <div class="source-card">

                            <div class="source-title">
                                {title}
                            </div>

                            <div class="source-meta">
                                {source} • {published}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if url:

                        st.link_button(
                            "Read original article",
                            url
                        )


            except Exception as e:

                st.error(
                    "Something went wrong while processing "
                    "your question."
                )

                st.exception(e)

