import re
import streamlit as st

from news_api import fetch_news
from gnews_api import fetch_gnews
from open_meteo_api import fetch_weather
from retrieval import retrieve_articles
from ai import generate_intelligence

from visualization import (
    generate_visualizations,
    render_visualizations_in_streamlit,
)


st.set_page_config(
    page_title="Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide",
)


st.title("🛰️ Real-Time Intelligence Platform")

st.markdown(
    """
    Ask questions about current events and get
    AI-powered intelligence based on recent news.
    """
)


with st.sidebar:
    st.header("⚙️ RTIP")

    st.markdown("### News Sources")
    st.checkbox(
        "NewsData.io",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "GNews",
        value=True,
        disabled=True,
    )

    st.markdown("### Intelligence")
    st.checkbox(
        "Source comparison",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "Conflict detection",
        value=True,
        disabled=True,
    )

    st.markdown("### Visualization")
    st.checkbox(
        "Auto-generated graphs",
        value=True,
        disabled=True,
    )

    st.divider()

    st.caption("Real-Time Intelligence Platform")


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
            re.IGNORECASE,
        )

        if match:
            location = match.group(1)
            location = location.strip(" ?!.,")
            return location

    return None


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

question = st.chat_input(
    "Ask about current events..."
)


if question:

    # -----------------------------------------------------
    # SHOW USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):
        st.write(question)


    # -----------------------------------------------------
    # WEATHER DETECTION
    # -----------------------------------------------------

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
        "how cold",
    ]


    is_weather_question = any(
        keyword in question.lower()
        for keyword in weather_keywords
    )


    # =====================================================
    # WEATHER BRANCH
    # =====================================================

    if is_weather_question:

        with st.chat_message("assistant"):

            try:

                location = extract_weather_location(
                    question
                )

                if not location:

                    st.warning(
                        "Please include a city or location."
                    )

                    st.info(
                        "Example: What is the weather in London?"
                    )

                    st.stop()


                with st.spinner(
                    f"🌦️ Getting weather for {location}..."
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
                    temperature_description = "very hot"

                elif temperature >= 30:
                    temperature_description = "hot"

                elif temperature >= 25:
                    temperature_description = "warm"

                elif temperature >= 18:
                    temperature_description = "mild"

                elif temperature >= 10:
                    temperature_description = "cool"

                else:
                    temperature_description = "cold"


                # Wind description

                if wind >= 30:
                    wind_description = "strong wind"

                elif wind >= 15:
                    wind_description = "moderate wind"

                else:
                    wind_description = "light wind"


                st.markdown(
                    f"""
🌦️ **{location.title()}:**
{temperature}°C with {humidity}% humidity
and {wind_description}.

The current conditions are relatively
{temperature_description}.
"""
                )


            except Exception:

                st.error(
                    "Something went wrong while "
                    "getting weather information."
                )

                st.exception(
                    Exception(
                        "Weather request failed."
                    )
                )


    # =====================================================
    # NEWS BRANCH
    # =====================================================

    else:

        with st.chat_message("assistant"):

            try:

                # -------------------------------------------------
                # STEP 1 — FETCH NEWS
                # -------------------------------------------------

                with st.spinner(
                    "🔎 Searching current news..."
                ):

                    newsdata_articles = fetch_news(
                        query=question,
                        language="en",
                        limit=15,
                    )


                    gnews_articles = fetch_gnews(
                        query=question,
                        language="en",
                        max_results=10,
                    )


                    articles = (
                        newsdata_articles
                        + gnews_articles
                    )


                # -------------------------------------------------
                # CHECK RESULTS
                # -------------------------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # -------------------------------------------------
                # STEP 2 — RETRIEVE RELEVANT ARTICLES
                # -------------------------------------------------

                with st.spinner(
                    "🧠 Finding the most relevant information..."
                ):

                    relevant_articles = retrieve_articles(
                        articles,
                        question,
                        max_articles=8,
                    )


                if not relevant_articles:

                    st.warning(
                        "No relevant articles were found."
                    )

                    st.stop()


                # -------------------------------------------------
                # STEP 3 — GEMINI INTELLIGENCE
                # -------------------------------------------------

                with st.spinner(
                    "🤖 Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles,
                    )


                # -------------------------------------------------
                # STEP 4 — DISPLAY AI ANSWER
                # -------------------------------------------------

                st.markdown(answer)


                # -------------------------------------------------
                # STEP 5 — VISUALIZATIONS
                # -------------------------------------------------

                with st.spinner(
                    "📊 Deciding which graphs are worth showing..."
                ):

                    viz_result = generate_visualizations(
                        relevant_articles,
                        question,
                        max_graphs=3,
                    )


                render_visualizations_in_streamlit(
                    viz_result
                )


                # -------------------------------------------------
                # STEP 6 — SOURCES
                # -------------------------------------------------

                st.divider()

                st.subheader("🔗 Sources")


                for article in relevant_articles:

                    title = article.get(
                        "title",
                        "Untitled",
                    )

                    source = article.get(
                        "source",
                        "Unknown source",
                    )

                    url = article.get("url")

                    published = article.get(
                        "published",
                        "Unknown date",
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
                    "Something went wrong while "
                    "processing your question."
                )

                st.exception(e)
