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
# SIMPLE COLOR / STYLE
# ==================================================

st.markdown(
    """
    <style>

    /* Overall page */

    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }


    /* Main content */

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* Main title */

    h1 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        white-space: nowrap;
    }


    /* Normal text */

    p {
        color: #cbd5e1;
    }


    /* Captions */

    .stCaption {
        color: #94a3b8 !important;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #080f1d;
        border-right: 1px solid #1e293b;
    }


    /* Sidebar headings */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }


    /* Chat messages */

    div[data-testid="stChatMessage"] {
        background-color: transparent;
    }


    /* User message */

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #111c32;
        border-radius: 14px;
        border: 1px solid #1e3a5f;
    }


    /* Assistant message */

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #0f172a;
        border-radius: 14px;
        border: 1px solid #1e293b;
    }


    /* Chat input */

    div[data-testid="stChatInput"] {
        background-color: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
    }


    div[data-testid="stChatInput"]:focus-within {
        border-color: #3b82f6;
    }


    /* Buttons */

    .stButton > button {
        background-color: #111827;
        color: #cbd5e1;
        border: 1px solid #334155;
        border-radius: 8px;
    }


    .stButton > button:hover {
        background-color: #172554;
        border-color: #3b82f6;
        color: #ffffff;
    }


    /* Metrics */

    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1rem;
    }


    /* Dividers */

    hr {
        border-color: #1e293b;
    }


    /* Links */

    a {
        color: #60a5fa !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.title(
    "🛰️ Real-Time Intelligence Platform"
)

st.caption(
    "Ask questions about current events and get "
    "AI-powered intelligence based on recent news."
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("RTIP")

    st.caption(
        "REAL-TIME INTELLIGENCE PLATFORM"
    )

    st.divider()

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
# CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# WELCOME
# ==================================================

if not st.session_state.messages:

    st.markdown(
        "## What is happening right now?"
    )

    st.write(
        "Ask about world events, politics, "
        "technology, conflicts, or breaking news."
    )


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

    # ----------------------------------------------
    # Store user message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ----------------------------------------------
    # User message
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # ----------------------------------------------
    # Detect weather
    # ----------------------------------------------

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


    # ==================================================
    # WEATHER
    # ==================================================

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

                st.subheader(
                    "Current Weather"
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


    # ==================================================
    # NEWS
    # ==================================================

    else:

        with st.chat_message("assistant"):

            try:

                # --------------------------------------
                # Get news
                # --------------------------------------

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


                # --------------------------------------
                # Check articles
                # --------------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # --------------------------------------
                # Retrieve
                # --------------------------------------

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


                # --------------------------------------
                # Generate intelligence
                # --------------------------------------

                with st.spinner(
                    "Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # --------------------------------------
                # Display answer
                # --------------------------------------

                st.markdown(
                    "### 🧠 Intelligence Brief"
                )

                st.markdown(answer)


                # --------------------------------------
                # Sources
                # --------------------------------------

                st.divider()

                st.subheader(
                    "Sources"
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

                    published = article.get(
                        "published",
                        "Unknown date"
                    )

                    url = article.get(
                        "url"
                    )


                    st.markdown(
                        f"**{title}**"
                    )

                    st.caption(
                        f"{source} • {published}"
                    )


                    if url:

                        st.link_button(
                            "Read original article",
                            url
                        )


                    st.divider()


            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "processing your question."
                )

                st.exception(e)

