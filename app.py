import re
import streamlit as st

from news_api import fetch_news
from gnews_api import fetch_gnews
from open_meteo_api import fetch_weather
from retrieval import retrieve_articles

from ai import (
    generate_concise_intelligence,
    generate_intelligence,
)

from visualization import (
    generate_visualizations,
    render_visualizations_in_streamlit,
)


st.set_page_config(
    page_title="RTIP - Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide",
)


# ---------------------------------------------------------
# WEATHER LOCATION EXTRACTION
# ---------------------------------------------------------

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
            return location.strip(" ?!.,")
    
    return None


# ---------------------------------------------------------
# WEATHER DETECTION
# ---------------------------------------------------------

def is_weather_question(question):
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
        "snow",
        "snowing",
        "sunny",
        "cloudy",
        "storm",
        "stormy",
        "degrees",
    ]

    question_lower = question.lower()

    return any(
        re.search(
            rf"\b{re.escape(keyword)}\b",
            question_lower
        )
        for keyword in weather_keywords
    )


# ---------------------------------------------------------
# SOURCE DISPLAY
# ---------------------------------------------------------

def render_sources(articles):
    st.subheader("🔗 Important Sources")

    for article in articles:
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
            "url",
            ""
        )

        st.markdown(f"**{title}**")
        st.caption(
            f"{source} • {published}"
        )

        if url:
            st.markdown(
                f"[Read original article]({url})"
            )

        st.divider()


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title(
    "🛰️ Real-Time Intelligence Platform"
)

st.write(
    "Ask about current events and receive "
    "AI-powered intelligence from recent news."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ RTIP Settings")

    # Location
    location = st.selectbox(
        "Select Location",
        [
            "Worldwide",
            "Pakistan",
            "India",
            "United States",
            "United Kingdom",
            "China",
            "Hyderabad, Pakistan",
            "Karachi, Pakistan",
            "Islamabad, Pakistan",
        ],
    )

    # Topic
    topic = st.selectbox(
        "Select Topic",
        [
            "Artificial Intelligence",
            "Technology",
            "Politics",
            "Business",
            "Education",
            "Health",
            "Sports",
            "Climate",
            "Cybersecurity",
            "World News",
        ],
    )

    # Answer mode
    answer_mode = st.radio(
        "Answer Mode",
        [
            "⚡ Smart Concise Intelligence",
            "📄 Detailed Intelligence Report",
        ],
    )

    # Article limit
    article_limit = st.slider(
        "Articles to retrieve",
        min_value=5,
        max_value=20,
        value=15,
    )

    st.divider()

    st.caption(
        "Real-Time Intelligence Platform"
    )


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask a question about current events..."
)


# ---------------------------------------------------------
# PROCESS QUESTION
# ---------------------------------------------------------

if question:

    # Show user message
    with st.chat_message("user"):
        st.write(question)

    # Assistant response
    with st.chat_message("assistant"):

        try:

            # =================================================
            # WEATHER BRANCH
            # =================================================

            if is_weather_question(question):

                location_from_question = (
                    extract_weather_location(question)
                )

                if not location_from_question:

                    st.warning(
                        "Please include a city or location."
                    )

                    st.info(
                        "Example: "
                        "What is the weather in London?"
                    )

                    st.stop()

                with st.spinner(
                    f"🌦️ Getting weather for "
                    f"{location_from_question}..."
                ):

                    weather = fetch_weather(
                        location=location_from_question
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

                st.markdown(
                    f"""
🌦️ **{location_from_question.title()}:**
{temperature}°C with {humidity}% humidity
and {wind_description}.

The current conditions are relatively
**{temperature_description}**.
"""
                )

            # =================================================
            # NEWS BRANCH
            # =================================================

            else:

                # ---------------------------------------------
                # Build news search query
                # ---------------------------------------------

                if location == "Worldwide":

                    search_query = (
                        f"{topic} {question}"
                    )

                else:

                    search_query = (
                        f"{location} "
                        f"{topic} "
                        f"{question}"
                    )

                # ---------------------------------------------
                # Fetch NewsData
                # ---------------------------------------------

                with st.spinner(
                    "🔎 Searching current news..."
                ):

                    newsdata_articles = fetch_news(
                        query=search_query,
                        language="en",
                        limit=article_limit,
                    )

                # ---------------------------------------------
                # Fetch GNews
                # ---------------------------------------------

                with st.spinner(
                    "🌐 Checking additional news sources..."
                ):

                    gnews_articles = fetch_gnews(
                        query=search_query,
                        language="en",
                        max_results=article_limit,
                    )

                # ---------------------------------------------
                # Combine sources
                # ---------------------------------------------

                articles = (
                    newsdata_articles
                    + gnews_articles
                )

                if not articles:

                    st.warning(
                        "No news articles were returned "
                        "by the news sources."
                    )

                    st.stop()

                # ---------------------------------------------
                # Retrieval / ranking / deduplication
                # ---------------------------------------------

                with st.spinner(
                    "🧠 Selecting the most relevant articles..."
                ):

                    relevant_articles = retrieve_articles(
                        articles,
                        question,
                        max_articles=8,
                    )

                # Safety fallback
                if not relevant_articles:

                    relevant_articles = articles[:8]

                if not relevant_articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()

                # ---------------------------------------------
                # Generate AI answer
                # ---------------------------------------------

                with st.spinner(
                    "🤖 Generating intelligence..."
                ):

                    if (
                        answer_mode
                        == "⚡ Smart Concise Intelligence"
                    ):

                        answer = (
                            generate_concise_intelligence(
                                question=question,
                                articles=relevant_articles,
                                location=location,
                                topic=topic,
                            )
                        )

                    else:

                        answer = (
                            generate_intelligence(
                                question=question,
                                articles=relevant_articles,
                                location=location,
                                topic=topic,
                            )
                        )

                # ---------------------------------------------
                # Display answer
                # ---------------------------------------------

                st.markdown(answer)

                # ---------------------------------------------
                # Visualization
                #
                # Only generate graphs in Detailed mode.
                # Concise mode stays clean.
                # ---------------------------------------------

                if (
                    answer_mode
                    == "📄 Detailed Intelligence Report"
                ):

                    with st.spinner(
                        "📊 Checking whether "
                        "visualizations are useful..."
                    ):

                        visualization_result = (
                            generate_visualizations(
                                relevant_articles,
                                question,
                                max_graphs=3,
                            )
                        )

                    render_visualizations_in_streamlit(
                        visualization_result
                    )

                # ---------------------------------------------
                # Sources
                # ---------------------------------------------

                render_sources(
                    relevant_articles
                )

        except Exception as error:

            st.error(
                "The request could not be completed."
            )

            st.exception(error)
