import streamlit as st

from news_api import fetch_news
from gnews_api import fetch_gnews
from open_meteo_api import fetch_weather
from retrieval import retrieve_articles
from ai import generate_intelligence, generate_advanced_research

from visualization import (
    generate_visualizations,
    render_visualizations_in_streamlit,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real-Time Intelligence Platform",
    page_icon="🛰️",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(
                circle at 50% -15%,
                #162a4a 0%,
                #0b1120 40%,
                #070c16 100%
            );
        color: #e2e8f0;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.2rem;
        padding-bottom: 5rem;
    }

    h1 {
        color: #f8fafc !important;
        font-size: 2.25rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.035em;
        white-space: nowrap;
        margin-bottom: 0.35rem !important;
    }

    h2,
    h3 {
        color: #f1f5f9 !important;
    }

    p {
        color: #cbd5e1;
    }

    .stCaption {
        color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #08111f 0%,
                #070c16 100%
            );
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] p {
        color: #94a3b8;
    }

    div[data-baseweb="select"] > div {
        background-color: #0f172a;
        border-color: #334155;
        border-radius: 9px;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #3b82f6;
    }

    div[role="radiogroup"] label {
        color: #cbd5e1;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 14px;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #101c31;
        border: 1px solid #1d3b63;
        box-shadow:
            0 4px 18px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stChatMessage"]:has(
        div[data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #0d1626;
        border: 1px solid #1e293b;
        box-shadow:
            0 4px 18px rgba(0, 0, 0, 0.14);
    }

    div[data-testid="stChatInput"] {
        background-color: #0d1728;
        border: 1px solid #334155;
        border-radius: 14px;
        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #3b82f6;
        box-shadow:
            0 0 0 1px #3b82f6,
            0 8px 30px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stMetric"] {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1rem;
    }

    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    .stButton > button {
        background-color: #111827;
        color: #cbd5e1;
        border: 1px solid #334155;
        border-radius: 9px;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background-color: #172554;
        border-color: #3b82f6;
        color: #ffffff;
    }

    hr {
        border-color: #1e293b;
    }

    a {
        color: #60a5fa !important;
    }

    a:hover {
        color: #93c5fd !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #070c16;
    }

    ::-webkit-scrollbar-thumb {
        background: #24344d;
        border-radius: 8px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #334d73;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.title("Real-Time Intelligence Platform")

st.caption(
    "Ask about the latest news, compare sources, explore developments, "
    "check weather, and get AI-powered intelligence."
)


# ============================================================
# SIDEBAR SETTINGS
# ============================================================

with st.sidebar:

    st.header("⚙️ Intelligence Settings")

    # --------------------------------------------------------
    # NEWS LOCATION
    # --------------------------------------------------------

    news_location = st.selectbox(
        "🌍 News Search Location",
        [
            "No specific location",
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

    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    topic = st.selectbox(
        "📰 Topic",
        [
            "All Topics",
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

    # --------------------------------------------------------
    # ANSWER MODE
    # --------------------------------------------------------

    answer_mode = st.radio(
        "🧠 Answer Mode",
        [
            "⚡ Smart Concise Intelligence",
            "📄 Detailed Intelligence Report",
            "🔬 Advanced Research / Challenging Answer",
        ],
        index=0,
    )

    # --------------------------------------------------------
    # ARTICLE LIMIT
    # --------------------------------------------------------

    if answer_mode == "⚡ Smart Concise Intelligence":

        article_limit = st.slider(
            "📚 Number of Articles to Analyze",
            min_value=5,
            max_value=15,
            value=8,
        )

    elif answer_mode == "📄 Detailed Intelligence Report":

        article_limit = st.slider(
            "📚 Number of Articles to Analyze",
            min_value=5,
            max_value=20,
            value=12,
        )

    else:

        article_limit = st.slider(
            "📚 Number of Articles to Analyze",
            min_value=8,
            max_value=25,
            value=18,
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
# WEATHER DISPLAY
# ============================================================

def show_weather(question_text):

    import re

    text = question_text.strip()

    patterns = [

        r"weather\s+(?:in|at|for)\s+(.+)",

        r"temperature\s+(?:in|at|for)\s+(.+)",

        r"forecast\s+(?:in|at|for)\s+(.+)",

        r"weather\s+(.+)",

        r"temperature\s+(.+)",

        r"forecast\s+(.+)",

        r"how(?:'s| is)\s+the\s+weather(?:\s+like)?\s+(?:in|at|for)\s+(.+)",

        r"what(?:'s| is)\s+the\s+weather(?:\s+like)?\s+(?:in|at|for)\s+(.+)",
    ]

    extracted_location = None

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            extracted_location = match.group(
                match.lastindex
            ).strip()

            break

    if extracted_location:

        extracted_location = (
            extracted_location
            .rstrip("?.!,")
            .strip()
        )

    if not extracted_location:

        st.warning(
            "Please include a location, for example: "
            "`What is the weather in London?`"
        )

        return

    with st.spinner(
        "🌤️ Getting weather information..."
    ):

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
                    (
                        f"{temperature} °C"
                        if temperature is not None
                        else "N/A"
                    ),
                )

            with col2:

                st.metric(
                    "Humidity",
                    (
                        f"{humidity}%"
                        if humidity is not None
                        else "N/A"
                    ),
                )

            with col3:

                st.metric(
                    "Wind",
                    (
                        f"{wind_speed} km/h"
                        if wind_speed is not None
                        else "N/A"
                    ),
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
        start=1,
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

        url = article.get("url")

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
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask about the latest news or weather..."
)


# ============================================================
# MAIN QUESTION PROCESSING
# ============================================================

if question:

    # ========================================================
    # WEATHER
    # ========================================================

    if is_weather_question(question):

        show_weather(question)

        st.stop()


    # ========================================================
    # BUILD NEWS SEARCH QUERY
    # ========================================================

    search_parts = []


    # Add location only if the user selected one
    if news_location not in [
        "No specific location",
        "Worldwide",
    ]:

        search_parts.append(
            news_location
        )


    # Add topic only if the user selected one
    if topic != "All Topics":

        search_parts.append(
            topic
        )


    # Always include the actual user question
    search_parts.append(
        question
    )


    search_query = " ".join(
        search_parts
    )


    # ========================================================
    # FETCH NEWS
    # ========================================================

    all_articles = []

    newsdata_error = None
    gnews_error = None


    # --------------------------------------------------------
    # NEWSDATA
    # --------------------------------------------------------

    with st.spinner(
        "📰 Searching NewsData..."
    ):

        try:

            newsdata_articles = fetch_news(
                query=search_query,
                language="en",
                limit=article_limit,
            )

            if newsdata_articles:

                all_articles.extend(
                    newsdata_articles
                )

        except Exception as error:

            newsdata_error = str(error)


    # --------------------------------------------------------
    # GNEWS
    # --------------------------------------------------------

    with st.spinner(
        "🌐 Searching GNews..."
    ):

        try:

            gnews_articles = fetch_gnews(
                query=search_query,
                language="en",
                max_results=article_limit,
            )

            if gnews_articles:

                all_articles.extend(
                    gnews_articles
                )

        except Exception as error:

            gnews_error = str(error)


    # ========================================================
    # NO ARTICLES
    # ========================================================

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


    # ========================================================
    # RETRIEVE MOST RELEVANT ARTICLES
    # ========================================================

    relevant_articles = retrieve_articles(
        all_articles,
        question,
        max_articles=article_limit,
    )


    if not relevant_articles:

        st.warning(
            "No relevant articles were found."
        )

        st.stop()


    # ========================================================
    # AI INTELLIGENCE
    # ========================================================

    st.subheader(
        "🧠 Intelligence"
    )


    try:

        with st.spinner(
            "🤖 Generating intelligence..."
        ):

            # ------------------------------------------------
            # CONCISE MODE
            # ------------------------------------------------

            if answer_mode == (
                "⚡ Smart Concise Intelligence"
            ):

                answer = generate_intelligence(
                    question,
                    relevant_articles,
                    concise=True,
                )


            # ------------------------------------------------
            # DETAILED MODE
            # ------------------------------------------------

            elif answer_mode == (
                "📄 Detailed Intelligence Report"
            ):

                answer = generate_intelligence(
                    question,
                    relevant_articles,
                    concise=False,
                )


            # ------------------------------------------------
            # ADVANCED RESEARCH MODE
            # ------------------------------------------------

            else:

                answer = generate_advanced_research(
                    question=question,
                    articles=relevant_articles,
                    location=news_location,
                    topic=topic,
                )


        st.markdown(answer)


    except Exception as error:

        st.error(
            f"Unable to generate intelligence: {error}"
        )

        st.stop()


    # ========================================================
    # VISUAL INTELLIGENCE
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Visual Intelligence"
    )


    try:

        with st.spinner(
            "📊 Checking whether visualizations are useful..."
        ):

            visualization_result = (
                generate_visualizations(
                    relevant_articles,
                    question,
                    max_graphs=3,
                )
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


    # ========================================================
    # SOURCES
    # ========================================================

    st.divider()

    render_sources(
        relevant_articles
    )
