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
    page_title="Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🛰️ Real-Time Intelligence Platform")

st.markdown(
    """
    Ask questions about current events and get
    AI-powered intelligence based on recent news.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ RTIP")

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


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask about current events..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # ----------------------------------------------
    # Display user question
    # ----------------------------------------------

    with st.chat_message("user"):
        st.write(question)


    # ----------------------------------------------
    # Detect question type
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


    # ==============================================
    # WEATHER QUESTION
    # ==============================================

    if is_weather_question:

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "🌦️ Getting current weather..."
                ):

                    weather = fetch_weather(
                        latitude=33.6844,
                        longitude=73.0479
                    )

                current = weather["current"]

                st.subheader(
                    "🌦️ Current Weather"
                )

                st.write(
                    f"🌡️ Temperature: "
                    f"{current['temperature_2m']} °C"
                )

                st.write(
                    f"💧 Humidity: "
                    f"{current['relative_humidity_2m']}%"
                )

                st.write(
                    f"💨 Wind: "
                    f"{current['wind_speed_10m']} km/h"
                )

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(e)


    # ==============================================
    # NEWS QUESTION
    # ==============================================

    else:

        with st.chat_message("assistant"):

            try:

                # ----------------------------------
                # STEP 1: Get news
                # ----------------------------------

                with st.spinner(
                    "🔎 Searching current news..."
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


                # ----------------------------------
                # Check articles
                # ----------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # ----------------------------------
                # STEP 2: Retrieve relevant articles
                # ----------------------------------

                with st.spinner(
                    "🧠 Finding the most relevant information..."
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


                # ----------------------------------
                # STEP 3: Generate AI intelligence
                # ----------------------------------

                with st.spinner(
                    "🤖 Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # ----------------------------------
                # STEP 4: Display AI answer
                # ----------------------------------

                st.markdown(answer)


                # ----------------------------------
                # STEP 5: Display sources
                # ----------------------------------

                st.divider()

                st.subheader("🔗 Sources")

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
                        f"**{title}**"
                    )

                    st.caption(
                        f"{source} • {published}"
                    )

                    if url:

                        st.markdown(
                            f"[Read original article]({url})"
                        )

                    st.divider()


            except Exception as e:

                st.error(
                    "Something went wrong while processing "
                    "your question."
                )

                st.exception(e)
