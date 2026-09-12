import re
import streamlit as st

from news_api import fetch_news
from gnews_api import fetch_gnews
from open_meteo_api import fetch_weather
from retrieval import retrieve_articles
from ai import generate_intelligence


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RTIP | Real-Time Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------- Global ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #0b1020 0%,
            #111827 50%,
            #0b1220 100%
        );
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- Header ---------- */

    .rtip-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(12px);
    }

    .rtip-brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .rtip-logo {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        font-size: 25px;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(129,140,248,0.25);
    }

    .rtip-title {
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin: 0;
    }

    .rtip-subtitle {
        color: #9ca3af;
        font-size: 0.82rem;
        margin-top: 3px;
    }

    .live-status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #d1d5db;
        letter-spacing: 1px;
    }

    .live-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 12px #22c55e;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: 0.45;
            transform: scale(0.8);
        }

        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* ---------- Welcome ---------- */

    .welcome-box {
        text-align: center;
        padding: 3rem 2rem 2rem;
        margin: 1rem 0 1.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        background:
            radial-gradient(
                circle at top,
                rgba(99,102,241,0.13),
                transparent 55%
            ),
            rgba(255,255,255,0.025);
    }

    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 0.7rem;
    }

    .welcome-title {
        font-size: 2.1rem;
        font-weight: 750;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: #9ca3af;
        font-size: 1rem;
        max-width: 650px;
        margin: auto;
    }

    /* ---------- Section Labels ---------- */

    .section-label {
        color: #9ca3af;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin: 1.2rem 0 0.7rem;
    }

    /* ---------- Intelligence Card ---------- */

    .intel-card {
        padding: 1.4rem;
        margin: 1rem 0;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.035);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    .intel-card h3 {
        margin-top: 0;
        font-size: 1rem;
    }

    .intel-card p {
        color: #cbd5e1;
        line-height: 1.7;
    }

    /* ---------- Source Cards ---------- */

    .source-card {
        padding: 1.1rem 1.2rem;
        margin: 0.8rem 0;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07);
        background: rgba(255,255,255,0.025);
        transition: all 0.2s ease;
    }

    .source-card:hover {
        transform: translateY(-2px);
        border-color: rgba(129,140,248,0.35);
        background: rgba(255,255,255,0.045);
    }

    .source-name {
        font-size: 0.75rem;
        font-weight: 700;
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .source-title {
        font-size: 1rem;
        font-weight: 650;
        margin: 0.4rem 0;
        line-height: 1.45;
    }

    .source-date {
        color: #6b7280;
        font-size: 0.75rem;
    }

    /* ---------- Quick Question Buttons ---------- */

    div.stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.09);
        background: rgba(255,255,255,0.04);
        color: #e5e7eb;
        padding: 0.7rem 1rem;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: rgba(129,140,248,0.5);
        background: rgba(99,102,241,0.12);
        transform: translateY(-2px);
    }

    /* ---------- Chat ---------- */

    [data-testid="stChatMessage"] {
        border-radius: 18px;
        margin-bottom: 0.8rem;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: #090e1a;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-status {
        padding: 1rem;
        border-radius: 14px;
        background: rgba(34,197,94,0.06);
        border: 1px solid rgba(34,197,94,0.12);
        margin-bottom: 1rem;
    }

    /* ---------- Hide Streamlit Branding ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="rtip-header">

        <div class="rtip-brand">

            <div class="rtip-logo">
                🛰️
            </div>

            <div>
                <div class="rtip-title">
                    RTIP
                </div>

                <div class="rtip-subtitle">
                    Real-Time Intelligence Platform
                </div>
            </div>

        </div>

        <div class="live-status">
            <span class="live-dot"></span>
            LIVE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🛰️ RTIP")

    st.markdown(
        """
        <div class="sidebar-status">
            <b>● System Online</b><br>
            <span style="color:#9ca3af;">
            Monitoring connected intelligence sources
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📡 Data Sources")

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

    st.checkbox(
        "Open-Meteo",
        value=True,
        disabled=True
    )

    st.divider()

    st.markdown("### 🧠 Intelligence")

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

    st.checkbox(
        "Relevance ranking",
        value=True,
        disabled=True
    )

    st.divider()

    st.caption(
        "RTIP v1.0 • Real-Time Intelligence"
    )


# --------------------------------------------------
# Weather Location Extraction
# --------------------------------------------------

def extract_weather_location(question):

    question = question.strip()

    patterns = [
        r"weather\s+(?:in|at|for|of)\s+(.+)",
        r"temperature\s+(?:in|at|for|of)\s+(.+)",
        r"forecast\s+(?:in|at|for|of)\s+(.+)",
        r"rain\s+(?:in|at|for|of)\s+(.+)",
        r"humidity\s+(?:in|at|for|of)\s+(.+)",
        r"wind\s+(?:in|at|for|of)\s+(.+)",
        r"hot\s+(?:in|at|for|of)\s+(.+)",
        r"cold\s+(?:in|at|for|of)\s+(.+)",
        r"sunny\s+(?:in|at|for|of)\s+(.+)",
        r"cloudy\s+(?:in|at|for|of)\s+(.+)",
        r"raining\s+(?:in|at|for|of)\s+(.+)",
        r"snow\s+(?:in|at|for|of)\s+(.+)",
        r"how hot\s+(?:is|in|at)\s+(.+)",
        r"how cold\s+(?:is|in|at)\s+(.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            question,
            re.IGNORECASE
        )

        if match:

            location = match.group(1)

            location = location.strip(
                " ?!.,"
            )

            return location

    return None


# --------------------------------------------------
# Welcome Screen
# --------------------------------------------------

st.markdown(
    """
    <div class="welcome-box">

        <div class="welcome-icon">
            🛰️
        </div>

        <div class="welcome-title">
            What's happening right now?
        </div>

        <div class="welcome-text">
            Search current events across multiple news
            sources and turn scattered headlines into
            clear intelligence.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Quick Questions
# --------------------------------------------------

st.markdown(
    '<div class="section-label">⚡ EXPLORE LIVE INTELLIGENCE</div>',
    unsafe_allow_html=True
)

quick_questions = [
    "🌍 Latest global news",
    "🇵🇰 What's happening in Pakistan?",
    "🤖 Latest AI news",
    "⚔️ Major world conflicts",
    "📈 Biggest stories today",
]

cols = st.columns(len(quick_questions))

for index, question_text in enumerate(quick_questions):

    with cols[index]:

        if st.button(
            question_text,
            use_container_width=True
        ):
            st.session_state["quick_question"] = (
                question_text
                .split(" ", 1)[1]
            )


# --------------------------------------------------
# Get Question
# --------------------------------------------------

question = st.chat_input(
    "Ask RTIP what's happening..."
)


# --------------------------------------------------
# Handle Quick Question
# --------------------------------------------------

if "quick_question" in st.session_state:

    question = st.session_state.pop(
        "quick_question"
    )


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # ----------------------------------------------
    # User Message
    # ----------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(question)


    # ----------------------------------------------
    # Question Detection
    # ----------------------------------------------

    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "raining",
        "wind",
        "windy",
        "humidity",
        "hot",
        "cold",
        "heat",
        "snow",
        "snowing",
        "sunny",
        "cloudy",
        "storm",
        "stormy",
        "degrees",
        "how hot",
        "how cold"
    ]

    is_weather_question = any(
        keyword in question.lower()
        for keyword in weather_keywords
    )


    # ==================================================
    # WEATHER
    # ==================================================

    if is_weather_question:

        with st.chat_message(
            "assistant",
            avatar="🛰️"
        ):

            try:

                location = extract_weather_location(
                    question
                )

                if not location:

                    st.warning(
                        "Please include a city or location."
                    )

                    st.info(
                        "Try: What is the weather in London?"
                    )

                    st.stop()


                with st.spinner(
                    f"🌦️ Checking live weather for {location}..."
                ):

                    weather = fetch_weather(
                        location=location
                    )


                current = weather["current"]

                temperature = current[
                    "temperature_2m"
                ]

                humidity = current[
                    "relative_humidity_2m"
                ]

                wind = current[
                    "wind_speed_10m"
                ]


                # Temperature description

                if temperature >= 35:

                    temperature_description = (
                        "very hot"
                    )

                elif temperature >= 30:

                    temperature_description = (
                        "hot"
                    )

                elif temperature >= 25:

                    temperature_description = (
                        "warm"
                    )

                elif temperature >= 18:

                    temperature_description = (
                        "mild"
                    )

                elif temperature >= 10:

                    temperature_description = (
                        "cool"
                    )

                else:

                    temperature_description = (
                        "cold"
                    )


                # Wind description

                if wind >= 30:

                    wind_description = (
                        "strong wind"
                    )

                elif wind >= 15:

                    wind_description = (
                        "moderate wind"
                    )

                else:

                    wind_description = (
                        "light wind"
                    )


                # Weather card

                st.markdown(
                    f"""
                    <div class="intel-card">

                        <h3>
                            🌦️ LIVE WEATHER
                        </h3>

                        <h2>
                            {location.title()}
                        </h2>

                        <p>
                            <b style="font-size:1.5rem;">
                            {temperature}°C
                            </b>
                        </p>

                        <p>
                            Current conditions are
                            <b>{temperature_description}</b>,
                            with {humidity}% humidity
                            and {wind_description}.
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(e)


    # ==================================================
    # NEWS
    # ==================================================

    else:

        with st.chat_message(
            "assistant",
            avatar="🛰️"
        ):

            try:

                # --------------------------------------
                # STEP 1: Retrieve News
                # --------------------------------------

                with st.spinner(
                    "📡 Connecting to live news sources..."
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


                # --------------------------------------
                # Check Results
                # --------------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # --------------------------------------
                # STEP 2: Retrieval
                # --------------------------------------

                with st.spinner(
                    "🔎 Cross-checking and ranking information..."
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


                # --------------------------------------
                # STEP 3: AI Analysis
                # --------------------------------------

                with st.spinner(
                    "🧠 Building intelligence brief..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # --------------------------------------
                # STEP 4: Intelligence Header
                # --------------------------------------

                st.markdown(
                    """
                    <div class="intel-card">

                        <h3>
                            🧠 INTELLIGENCE BRIEF
                        </h3>

                        <p>
                            Analysis generated from
                            multiple current news sources.
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # --------------------------------------
                # STEP 5: AI Answer
                # --------------------------------------

                st.markdown(answer)


                # --------------------------------------
                # STEP 6: Sources
                # --------------------------------------

                st.markdown(
                    '<div class="section-label">📰 SOURCES</div>',
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

                    url = article.get(
                        "url"
                    )

                    published = article.get(
                        "published",
                        "Unknown date"
                    )

                    description = article.get(
                        "description",
                        ""
                    )

                    if description:

                        description = (
                            description[:180]
                            + "..."
                            if len(description) > 180
                            else description
                        )


                    source_card = f"""
                    <div class="source-card">

                        <div class="source-name">
                            📰 {source}
                        </div>

                        <div class="source-title">
                            {title}
                        </div>

                        <div class="source-date">
                            🕐 {published}
                        </div>

                    """

                    if description:

                        source_card += f"""
                        <div style="
                            color:#9ca3af;
                            font-size:0.85rem;
                            margin-top:0.5rem;
                            line-height:1.5;
                        ">
                            {description}
                        </div>
                        """


                    if url:

                        source_card += f"""
                        <div style="
                            margin-top:0.8rem;
                        ">
                            <a
                                href="{url}"
                                target="_blank"
                                style="
                                    color:#a5b4fc;
                                    text-decoration:none;
                                    font-weight:600;
                                    font-size:0.85rem;
                                "
                            >
                                Read original article →
                            </a>
                        </div>
                        """


                    source_card += "</div>"


                    st.markdown(
                        source_card,
                        unsafe_allow_html=True
                    )


            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "processing your question."
                )

                st.exception(e)
