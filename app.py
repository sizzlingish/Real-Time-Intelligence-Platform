import re
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
    page_title="RTIP | Real-Time Intelligence",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ------------------------------
       Main background
    ------------------------------ */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(79, 70, 229, 0.10),
                transparent 35%
            ),
            #0b1020;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }


    /* ------------------------------
       Header
    ------------------------------ */

    .rtip-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;

        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;

        background: rgba(255,255,255,0.035);
        backdrop-filter: blur(10px);
    }

    .rtip-brand {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .rtip-logo {
        width: 48px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(129,140,248,0.25);

        font-size: 25px;
    }

    .rtip-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #f8fafc;
    }

    .rtip-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 2px;
    }


    /* ------------------------------
       Live indicator
    ------------------------------ */

    .live-status {
        display: flex;
        align-items: center;
        gap: 8px;

        color: #d1d5db;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.3px;
    }

    .live-dot {
        width: 9px;
        height: 9px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 8px rgba(34,197,94,0.8);

        animation: livePulse 1.8s infinite;
    }

    @keyframes livePulse {

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


    /* ------------------------------
       Welcome area
    ------------------------------ */

    .welcome-box {
        text-align: center;

        padding: 2.8rem 1.5rem 2.3rem;

        margin-bottom: 1.4rem;

        border-radius: 22px;

        border: 1px solid rgba(255,255,255,0.07);

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(99,102,241,0.14),
                transparent 55%
            ),
            rgba(255,255,255,0.025);
    }

    .welcome-icon {
        font-size: 2.8rem;
        margin-bottom: 0.7rem;
    }

    .welcome-title {
        font-size: 2rem;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        color: #94a3b8;
        max-width: 650px;
        margin: auto;
        line-height: 1.6;
    }


    /* ------------------------------
       Section labels
    ------------------------------ */

    .section-label {
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 1.5px;
        color: #94a3b8;

        margin-top: 1.1rem;
        margin-bottom: 0.7rem;
    }


    /* ------------------------------
       Intelligence cards
    ------------------------------ */

    .intel-card {
        padding: 1.2rem;

        border-radius: 17px;

        border: 1px solid rgba(255,255,255,0.07);

        background: rgba(255,255,255,0.035);

        margin-bottom: 0.8rem;
    }


    /* ------------------------------
       Source cards
    ------------------------------ */

    .source-card {
        padding: 1rem 1.1rem;

        margin-bottom: 0.8rem;

        border-radius: 16px;

        border: 1px solid rgba(255,255,255,0.07);

        background: rgba(255,255,255,0.025);

        transition: all 0.2s ease;
    }

    .source-card:hover {
        transform: translateY(-2px);

        border-color:
            rgba(129,140,248,0.4);

        background:
            rgba(255,255,255,0.045);
    }

    .source-name {
        font-size: 0.72rem;
        font-weight: 750;

        color: #a5b4fc;

        text-transform: uppercase;

        letter-spacing: 0.8px;
    }

    .source-title {
        color: #f1f5f9;

        font-size: 0.98rem;

        font-weight: 650;

        line-height: 1.45;

        margin-top: 0.35rem;
    }

    .source-description {
        color: #94a3b8;

        font-size: 0.82rem;

        line-height: 1.5;

        margin-top: 0.5rem;
    }

    .source-date {
        color: #64748b;

        font-size: 0.72rem;

        margin-top: 0.45rem;
    }


    /* ------------------------------
       Buttons
    ------------------------------ */

    div.stButton > button {

        border-radius: 13px;

        border: 1px solid
            rgba(255,255,255,0.08);

        background:
            rgba(255,255,255,0.035);

        color: #e2e8f0;

        min-height: 44px;

        transition: all 0.2s ease;
    }

    div.stButton > button:hover {

        border-color:
            rgba(129,140,248,0.45);

        background:
            rgba(99,102,241,0.10);

        transform: translateY(-2px);
    }


    /* ------------------------------
       Chat messages
    ------------------------------ */

    [data-testid="stChatMessage"] {

        border-radius: 18px;

        margin-bottom: 0.7rem;
    }


    /* ------------------------------
       Sidebar
    ------------------------------ */

    [data-testid="stSidebar"] {

        background: #080d19;

        border-right:
            1px solid
            rgba(255,255,255,0.06);
    }


    /* ------------------------------
       Hide Streamlit menu/footer
    ------------------------------ */

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


# ==================================================
# HEADER
# ==================================================

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


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🛰️ RTIP")

    st.success("● System Online")

    st.caption(
        "Monitoring connected intelligence sources"
    )

    st.divider()

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


# ==================================================
# WEATHER LOCATION EXTRACTION
# ==================================================

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


# ==================================================
# WELCOME SCREEN
# ==================================================

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
            Search current events across multiple
            news sources and turn scattered headlines
            into clear intelligence.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# QUICK QUESTIONS
# ==================================================

st.markdown(
    '<div class="section-label">⚡ EXPLORE LIVE INTELLIGENCE</div>',
    unsafe_allow_html=True
)


quick_questions = [
    "🌍 Global headlines",
    "🇵🇰 Pakistan news",
    "🤖 Latest AI news",
    "⚔️ World conflicts",
    "📈 Biggest stories",
]


quick_cols = st.columns(5)


for index, quick_question in enumerate(
    quick_questions
):

    with quick_cols[index]:

        if st.button(
            quick_question,
            use_container_width=True
        ):

            st.session_state[
                "selected_question"
            ] = quick_question


# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input(
    "Ask RTIP what's happening..."
)


# ==================================================
# QUICK QUESTION HANDLER
# ==================================================

if (
    not question
    and "selected_question"
    in st.session_state
):

    question = st.session_state.pop(
        "selected_question"
    )


# ==================================================
# PROCESS QUESTION
# ==================================================

if question:

    # ------------------------------------------------
    # USER MESSAGE
    # ------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(question)


    # ------------------------------------------------
    # WEATHER DETECTION
    # ------------------------------------------------

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

        for keyword
        in weather_keywords

    )


    # ==================================================
    # WEATHER QUESTION
    # ==================================================

    if is_weather_question:

        with st.chat_message(
            "assistant",
            avatar="🛰️"
        ):

            try:

                location = (
                    extract_weather_location(
                        question
                    )
                )


                if not location:

                    st.warning(
                        "Please include a city or location."
                    )

                    st.info(
                        "Try: What is the weather in London?"
                    )

                    st.stop()


                # ------------------------------------
                # Fetch weather
                # ------------------------------------

                with st.spinner(
                    f"🌦️ Checking live weather for {location}..."
                ):

                    weather = fetch_weather(
                        location=location
                    )


                current = weather[
                    "current"
                ]


                temperature = current[
                    "temperature_2m"
                ]

                humidity = current[
                    "relative_humidity_2m"
                ]

                wind = current[
                    "wind_speed_10m"
                ]


                # ------------------------------------
                # Temperature description
                # ------------------------------------

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


                # ------------------------------------
                # Wind description
                # ------------------------------------

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


                # ------------------------------------
                # Weather UI
                # ------------------------------------

                st.markdown(
                    '<div class="intel-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 🌦️ LIVE WEATHER"
                )

                st.markdown(
                    f"## {location.title()}"
                )

                st.metric(
                    "Temperature",
                    f"{temperature}°C"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Humidity",
                        f"{humidity}%"
                    )

                with col2:

                    st.metric(
                        "Wind",
                        f"{wind} km/h"
                    )

                st.info(
                    f"Current conditions are "
                    f"**{temperature_description}** "
                    f"with **{wind_description}**."
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(e)


    # ==================================================
    # NEWS QUESTION
    # ==================================================

    else:

        with st.chat_message(
            "assistant",
            avatar="🛰️"
        ):

            try:

                # --------------------------------------
                # STEP 1 — NEWS APIs
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
                # Check articles
                # --------------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # --------------------------------------
                # STEP 2 — RETRIEVAL
                # --------------------------------------

                with st.spinner(
                    "🔎 Cross-checking and ranking information..."
                ):

                    relevant_articles = (
                        retrieve_articles(
                            articles,
                            question,
                            max_articles=8
                        )
                    )


                if not relevant_articles:

                    st.warning(
                        "No relevant articles were found."
                    )

                    st.stop()


                # --------------------------------------
                # STEP 3 — GEMINI
                # --------------------------------------

                with st.spinner(
                    "🧠 Building intelligence brief..."
                ):

                    answer = (
                        generate_intelligence(
                            question,
                            relevant_articles
                        )
                    )


                # --------------------------------------
                # INTELLIGENCE HEADER
                # --------------------------------------

                st.markdown(
                    '<div class="intel-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 🧠 INTELLIGENCE BRIEF"
                )

                st.caption(
                    "Analysis generated from multiple "
                    "current news sources."
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


                # --------------------------------------
                # AI RESPONSE
                # --------------------------------------

                st.markdown(answer)


                # --------------------------------------
                # SOURCE SECTION
                # --------------------------------------

                st.markdown(
                    '<div class="section-label">'
                    '📰 SOURCES'
                    '</div>',
                    unsafe_allow_html=True
                )


                # --------------------------------------
                # SOURCE CARDS
                # --------------------------------------

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

                        if len(description) > 180:

                            description = (
                                description[:180]
                                + "..."
                            )


                    # ----------------------------------
                    # Card
                    # ----------------------------------

                    st.markdown(
                        '<div class="source-card">',
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        f"""
                        <div class="source-name">
                            📰 {source}
                        </div>

                        <div class="source-title">
                            {title}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if description:

                        st.markdown(
                            f"""
                            <div class="source-description">
                                {description}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    st.markdown(
                        f"""
                        <div class="source-date">
                            🕐 {published}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    if url:

                        st.link_button(
                            "Read original article →",
                            url,
                            use_container_width=False
                        )


                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )


            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "processing your question."
                )

                st.exception(e)
