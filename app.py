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
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #777;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #777;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .status {
        font-size: 0.85rem;
        color: #16a34a;
        font-weight: 600;
    }

    .intelligence-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        '<div class="main-title">🛰️ Real-Time Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Ask questions about current events and get '
        'AI-powered intelligence based on recent news.'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        '<div class="status">● LIVE</div>',
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("RTIP")

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
# Quick Questions
# --------------------------------------------------

st.markdown(
    '<div class="section-title">QUICK QUESTIONS</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

quick_question = None

with col1:
    if st.button(
        "Global News",
        use_container_width=True
    ):
        quick_question = "What is the latest world news?"

with col2:
    if st.button(
        "Pakistan News",
        use_container_width=True
    ):
        quick_question = "What is the latest news in Pakistan?"

with col3:
    if st.button(
        "AI News",
        use_container_width=True
    ):
        quick_question = "What are the latest developments in artificial intelligence?"

with col4:
    if st.button(
        "World Conflicts",
        use_container_width=True
    ):
        quick_question = "What are the latest developments in major world conflicts?"


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask about current events..."
)


# --------------------------------------------------
# Use Quick Question If Selected
# --------------------------------------------------

if quick_question:
    question = quick_question


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # ----------------------------------------------
    # Display User Question
    # ----------------------------------------------

    with st.chat_message("user"):
        st.write(question)


    # ----------------------------------------------
    # Detect Question Type
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

                temp_col, humidity_col, wind_col = st.columns(3)

                with temp_col:
                    st.metric(
                        "Temperature",
                        f"{current['temperature_2m']} °C"
                    )

                with humidity_col:
                    st.metric(
                        "Humidity",
                        f"{current['relative_humidity_2m']}%"
                    )

                with wind_col:
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


    # ==============================================
    # NEWS QUESTION
    # ==============================================

    else:

        with st.chat_message("assistant"):

            try:

                # ----------------------------------
                # STEP 1: Get News
                # ----------------------------------

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


                # ----------------------------------
                # Check Articles
                # ----------------------------------

                if not articles:

                    st.warning(
                        "No relevant news articles were found."
                    )

                    st.stop()


                # ----------------------------------
                # STEP 2: Retrieve Relevant Articles
                # ----------------------------------

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


                # ----------------------------------
                # STEP 3: Generate AI Intelligence
                # ----------------------------------

                with st.spinner(
                    "Analyzing the information..."
                ):

                    answer = generate_intelligence(
                        question,
                        relevant_articles
                    )


                # ----------------------------------
                # STEP 4: Intelligence Answer
                # ----------------------------------

                st.markdown(
                    "### Intelligence Brief"
                )

                st.markdown(answer)


                # ----------------------------------
                # STEP 5: Sources
                # ----------------------------------

                st.divider()

                st.subheader("Sources")

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

                    with st.container(
                        border=True
                    ):

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


            except Exception as e:

                st.error(
                    "Something went wrong while processing "
                    "your question."
                )

                st.exception(e)

