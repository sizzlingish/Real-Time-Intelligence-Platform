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


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🛰️ Real-Time Intelligence Platform")

st.caption(
    "Ask about the latest news, compare sources, explore developments, "
    "and get AI-powered intelligence."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Intelligence Settings")

    location = st.selectbox(
        "🌍 Location",
        [
            "Worldwide",
            "Pakistan",
            "India",
            "US",
            "UK",
            "China",
            "Hyderabad",
            "Karachi",
            "Islamabad",
        ],
        index=0,
    )

    topic = st.selectbox(
        "📰 Topic",
        [
            "AI",
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
        index=0,
    )

    answer_mode = st.radio(
        "🧠 Answer Mode",
        [
            "⚡ Smart Concise Intelligence",
            "📄 Detailed Intelligence Report",
        ],
        index=0,
    )

    article_limit = st.slider(
        "📚 Articles to retrieve",
        min_value=5,
        max_value=20,
        value=15,
    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about the latest news..."
)


# ============================================================
# WEATHER DETECTION
# ============================================================

def is_weather_question(text):
    weather_words = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "raining",
        "humidity",
        "wind",
        "hot",
        "cold",
    ]

    text = text.lower()

    return any(
        word in text
        for word in weather_words
    )


# ============================================================
# WEATHER RESPONSE
# ============================================================

def show_weather(question_text):

    # Try to extract a likely location from common patterns.

    location_text = question_text.lower()

    prefixes = [
        "what is the weather in ",
        "what's the weather in ",
        "weather in ",
        "temperature in ",
        "forecast in ",
        "how is the weather in ",
    ]

    extracted_location = None

    for prefix in prefixes:
        if prefix in location_text:
            extracted_location = location_text.split(
                prefix,
                1
            )[1].strip()

            break

    if not extracted_location:

        st.warning(
            "Please include a location, for example: "
            "`What is the weather in Islamabad?`"
        )

        return

    with st.spinner("🌤️ Getting weather information..."):

        try:

            weather_data = fetch_weather(
                location=extracted_location
            )

            current = weather_data.get(
                "current",
                {}
            )

            temperature = current.get(
                "temperature_2m"
            )

            humidity = current.get(
                "relative_humidity_2m"
            )

            wind_speed = current.get(
                "wind_speed_10m"
            )

            weather_code = current.get(
                "weather_code"
            )

            st.subheader(
                f"🌤️ Weather in {extracted_location.title()}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Temperature",
                    f"{temperature} °C"
                    if temperature is not None
                    else "N/A",
                )

            with col2:
                st.metric(
                    "Humidity",
                    f"{humidity}%"
                    if humidity is not None
                    else "N/A",
                )

            with col3:
                st.metric(
                    "Wind",
                    f"{wind_speed} km/h"
                    if wind_speed is not None
                    else "N/A",
                )

            if weather_code is not None:

                st.caption(
                    f"Weather code: {weather_code}"
                )

        except Exception as error:

            st.error(
                f"Unable to retrieve weather information: {error}"
            )


# ============================================================
# SOURCE DISPLAY
# ============================================================

def render_sources(articles):

    if not articles:
        return

    st.subheader("📚 Sources")

    for index, article in enumerate(
        articles,
        start=1
    ):

        title = article.get(
            "title",
            "Untitled article"
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

        source_text = (
            f"**{index}. {title}**  \n"
            f"{source} • {published}"
        )

        if url:

            st.markdown(
                f"{source_text}  \n"
                f"[Read article]({url})"
            )

        else:

            st.markdown(
                source_text
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

if question:

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    if is_weather_question(question):

        show_weather(question)

        st.stop()


    # --------------------------------------------------------
    # NEWS SEARCH
    # --------------------------------------------------------

    if location == "Worldwide":

        search_query = (
            f"{topic} {question}"
        )

    else:

        search_query = (
            f"{location} {topic} {question}"
        )


    # --------------------------------------------------------
    # FETCH NEWS FROM MULTIPLE SOURCES
    # --------------------------------------------------------

    all_articles = []

    newsdata_error = None
    gnews_error = None


    # NewsData

    with st.spinner(
        "📰 Searching NewsData..."
    ):

        try:

            newsdata_articles = fetch_news(
                query=search_query,
                language="en",
                limit=article_limit,
            )

            all_articles.extend(
                newsdata_articles
            )

        except Exception as error:

            newsdata_error = str(error)


    # GNews

    with st.spinner(
        "🌐 Searching GNews..."
    ):

        try:

            gnews_articles = fetch_gnews(
                query=search_query,
                language="en",
                max_results=article_limit,
            )

            all_articles.extend(
                gnews_articles
            )

        except Exception as error:

            gnews_error = str(error)


    # --------------------------------------------------------
    # CHECK RESULTS
    # --------------------------------------------------------

    if not all_articles:

        st.error(
            "No news articles were retrieved."
        )

        if newsdata_error:

            st.caption(
                f"NewsData: {newsdata_error}"
            )

        if gnews_error:

            st.caption(
                f"GNews: {gnews_error}"
            )

        st.stop()


    # --------------------------------------------------------
    # RETRIEVE MOST RELEVANT ARTICLES
    # --------------------------------------------------------

    relevant_articles = retrieve_articles(
        all_articles,
        question,
        max_articles=8,
    )


    if not relevant_articles:

        st.warning(
            "No relevant articles were found."
        )

        st.stop()


    # --------------------------------------------------------
    # AI INTELLIGENCE
    # --------------------------------------------------------

    st.subheader("🧠 Intelligence")


    try:

        with st.spinner(
            "🤖 Generating intelligence..."
        ):

            # IMPORTANT:
            #
            # Concise and Detailed modes are handled
            # here.
            #
            # The ai.py file will later receive the
            # `concise` parameter.
            #
            # For now, this keeps the app compatible
            # with the current generate_intelligence()
            # function.

            answer = generate_intelligence(
                question,
                relevant_articles,
            )

        st.markdown(answer)

    except Exception as error:

        st.error(
            f"Unable to generate intelligence: {error}"
        )

        st.stop()


    # --------------------------------------------------------
    # VISUALIZATIONS
    # --------------------------------------------------------
    #
    # IMPORTANT:
    #
    # Charts are intentionally OUTSIDE the answer_mode
    # condition.
    #
    # Therefore charts can appear in BOTH:
    #
    # ⚡ Concise
    # 📄 Detailed
    #
    # The visualization system itself decides whether
    # a chart is useful.
    #

    st.divider()

    st.subheader("📊 Visual Intelligence")

    try:

        with st.spinner(
            "📊 Checking whether visualizations are useful..."
        ):

            visualization_result = generate_visualizations(
                relevant_articles,
                question,
                max_graphs=3,
            )


        if visualization_result:

            render_visualizations_in_streamlit(
                visualization_result
            )

        else:

            st.info(
                "No meaningful visualization was found "
                "for this question and the available data."
            )

    except Exception as error:

        st.warning(
            f"Visualization could not be generated: {error}"
        )


    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------
    #
    # Sources are also outside the answer-mode condition.
    #
    # Therefore BOTH modes show sources.
    #

    st.divider()

    render_sources(
        relevant_articles
    )

