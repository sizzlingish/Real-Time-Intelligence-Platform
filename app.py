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
# VISUAL STYLE
# ==================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 0%,
                rgba(37, 99, 235, 0.12),
                transparent 32%
            ),
            radial-gradient(
                circle at 10% 10%,
                rgba(14, 165, 233, 0.07),
                transparent 28%
            );
    }


    /* Main content width */

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }


    /* Chat messages */

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
    }


    /* Chat input */

    div[data-testid="stChatInput"] {
        border-radius: 14px;
    }


    /* Buttons */

    .stButton > button {
        border-radius: 10px;
    }


    /* Divider */

    hr {
        opacity: 0.2;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

header_left, header_right = st.columns(
    [6, 1]
)

with header_left:

    st.markdown(
        "# 🛰️ Real-Time Intelligence Platform"
    )

    st.caption(
        "Ask questions about current events and get "
        "AI-powered intelligence based on recent news."
    )


with header_right:

    st.markdown(
        "🟢 **LIVE**"
    )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("RTIP")

    st.caption(
        "REAL-TIME INTELLIGENCE"
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
# WELCOME SCREEN
# ==================================================

if not st.session_state.messages:

    st.markdown(
        "## 🛰️ What is happening right now?"
    )

    st.write(
        "Ask about world events, politics, "
        "technology, conflicts, or breaking news."
    )

    st.divider()


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
    # Display user message
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # ----------------------------------------------
    # Detect weather question
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

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "Getting current weather..."
                ):

                    weather = fetch_weather(
                        latitude=33.6844,
                        longitude=73.0479
                    )

                current = weather["current"]

                st.markdown(
                    "### 🌦️ Current Weather"
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

            with st.chat_message("assistant"):

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(e)


    # ==================================================
    # NEWS
    # ==================================================

    else:

        try:

            with st.chat_message("assistant"):

                # --------------------------------------
                # Search news
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
                # No articles
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
                # Gemini
                # --------------------------------------

                with st.spinner(
                    "Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # --------------------------------------
                # Intelligence Brief
                # --------------------------------------

                st.markdown(
                    "## 🧠 Intelligence Brief"
                )

                st.markdown(answer)


                # --------------------------------------
                # Sources
                # --------------------------------------

                st.divider()

                st.markdown(
                    "### 🔗 Sources"
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

                    url = article.get("url")


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

            with st.chat_message("assistant"):

                st.error(
                    "Something went wrong while "
                    "processing your question."
                )

                st.exception(e)

