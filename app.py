import re
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
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Real-Time Intelligence Platform",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# DARK UI STYLING
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .stTextInput input {
        background-color: #161b22;
        color: white;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #161b22;
        color: white;
    }

    .stRadio label {
        color: white;
    }

    .source-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }

    .source-card a {
        color: #58a6ff;
        text-decoration: none;
    }

    .weather-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }

    .search-query {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 10px 0 20px 0;
        color: #c9d1d9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.title("🧠 Real-Time Intelligence Platform")

st.markdown(
    """
    Ask a question and the platform will retrieve recent news,
    analyze the evidence, compare sources, and generate intelligence.
    Weather questions are handled automatically.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Intelligence Settings")

    news_location = st.selectbox(
        "🌍 News Search Location",
        [
            "No specific location",
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
        help="This setting affects news searches only. Weather location comes from your question.",
    )

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

    answer_mode = st.radio(
        "🧠 Answer Mode",
        [
            "⚡ Smart Concise Intelligence",
            "📄 Detailed Intelligence Report",
            "🔬 Advanced Research / Challenging Answer",
        ],
        index=0,
    )

    if answer_mode == "⚡ Smart Concise Intelligence":
        default_articles = 8
        max_articles = 15

    elif answer_mode == "📄 Detailed Intelligence Report":
        default_articles = 12
        max_articles = 20

    else:
        default_articles = 18
        max_articles = 25

    article_limit = st.slider(
        "📚 Number of Articles to Analyze",
        min_value=5,
        max_value=max_articles,
        value=default_articles,
    )

    st.divider()

    st.caption(
        "💡 Weather searches are automatic. "
        "Try: “What is the weather in London?”"
    )


# ============================================================
# WEATHER DETECTION
# ============================================================

def is_weather_question(text):
    """
    Detect whether the user's question is about weather.
    """

    weather_words = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "raining",
        "humidity",
        "wind",
        "windy",
        "hot",
        "cold",
        "snow",
        "storm",
        "sunny",
        "cloudy",
    ]

    text = text.lower()

    return any(
        re.search(r"\b" + re.escape(word) + r"\b", text)
        for word in weather_words
    )


# ============================================================
# WEATHER LOCATION EXTRACTION
# ============================================================

def extract_weather_location(question):
    """
    Extract a likely location from common weather questions.

    Examples:
        weather in London
        temperature in Karachi
        forecast for Islamabad
        weather of New York
    """

    patterns = [
        r"\bweather\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\btemperature\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bforecast\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\braining\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bwind\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bhumidity\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bhot\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bcold\s+(?:in|at|for|of)\s+(.+?)(?:\?|$)",
        r"\bweather\s+(?:today|tomorrow)\s+(?:in|at|for)\s+(.+?)(?:\?|$)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            question,
            flags=re.IGNORECASE,
        )

        if match:
            location = match.group(1).strip()

            # Remove common trailing phrases.
            location = re.sub(
                r"\b(today|tomorrow|right now|now)\b",
                "",
                location,
                flags=re.IGNORECASE,
            )

            location = location.strip(" ,.")

            if location:
                return location

    return None


# ============================================================
# WEATHER DISPLAY
# ============================================================

def show_weather(question):

    weather_location = extract_weather_location(question)

    if not weather_location:
        st.warning(
            "I detected a weather question, but I couldn't determine "
            "the location. Try something like: "
            "“What is the weather in London?”"
        )
        return

    st.subheader(f"🌤️ Weather — {weather_location}")

    try:
        weather_data = fetch_weather(
            location=weather_location
        )

        current = weather_data.get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")

        st.markdown(
            '<div class="weather-card">',
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if temperature is not None:
                st.metric(
                    "🌡️ Temperature",
                    f"{temperature} °C",
                )
            else:
                st.metric(
                    "🌡️ Temperature",
                    "N/A",
                )

        with col2:
            if humidity is not None:
                st.metric(
                    "💧 Humidity",
                    f"{humidity}%",
                )
            else:
                st.metric(
                    "💧 Humidity",
                    "N/A",
                )

        with col3:
            if wind_speed is not None:
                st.metric(
                    "💨 Wind Speed",
                    f"{wind_speed} km/h",
                )
            else:
                st.metric(
                    "💨 Wind Speed",
                    "N/A",
                )

        with col4:
            if weather_code is not None:
                st.metric(
                    "☁️ Weather Code",
                    str(weather_code),
                )
            else:
                st.metric(
                    "☁️ Weather Code",
                    "N/A",
                )

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(
            f"Weather request failed: {e}"
        )


# ============================================================
# NEWS QUERY CLEANING
# ============================================================

def build_news_search_query(question, location, topic):
    """
    Convert a natural-language user question into a short,
    API-friendly news search query.

    The original question is NOT changed. This function only
    creates the query sent to NewsData and GNews.
    """

    # Remove URLs.
    query = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        question,
        flags=re.IGNORECASE,
    )

    # Replace punctuation with spaces.
    query = re.sub(
        r"[^\w\s-]",
        " ",
        query,
    )

    query = query.lower()

    # Common conversational/search-stop words.
    stop_words = {
        "what",
        "what's",
        "whats",
        "why",
        "how",
        "when",
        "where",
        "who",
        "which",
        "whose",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "do",
        "does",
        "did",
        "can",
        "could",
        "will",
        "would",
        "should",
        "may",
        "might",
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "if",
        "then",
        "than",
        "to",
        "of",
        "for",
        "in",
        "on",
        "at",
        "by",
        "with",
        "from",
        "into",
        "about",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "they",
        "their",
        "them",
        "we",
        "our",
        "you",
        "your",
        "i",
        "me",
        "my",
        "recent",
        "reports",
        "report",
        "suggest",
        "suggests",
        "according",
        "latest",
        "currently",
        "current",
    }

    words = query.split()

    important_words = [
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
    ]

    # Remove duplicate words while preserving order.
    unique_words = []

    for word in important_words:
        if word not in unique_words:
            unique_words.append(word)

    # Add sidebar location only when explicitly selected.
    if location not in [
        "No specific location",
        "Worldwide",
        "",
        None,
    ]:
        location_words = re.sub(
            r"[^\w\s-]",
            " ",
            location.lower(),
        ).split()

        for word in location_words:
            if word not in unique_words:
                unique_words.insert(0, word)

    # Add selected topic when not "All Topics".
    if topic not in [
        "All Topics",
        "",
        None,
    ]:
        topic_words = re.sub(
            r"[^\w\s-]",
            " ",
            topic.lower(),
        ).split()

        for word in reversed(topic_words):
            if word not in unique_words:
                unique_words.insert(0, word)

    # Keep news API queries reasonably short.
    unique_words = unique_words[:12]

    search_query = " ".join(unique_words).strip()

    return search_query


# ============================================================
# SOURCE DISPLAY
# ============================================================

def render_sources(articles):

    if not articles:
        return

    st.subheader("📰 Sources")

    for article in articles:

        title = article.get(
            "title",
            "Untitled",
        )

        source = article.get(
            "source",
            "Unknown source",
        )

        published = article.get(
            "published",
            "Unknown date",
        )

        url = article.get(
            "url",
            "",
        )

        st.markdown(
            '<div class="source-card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"**{title}**"
        )

        st.caption(
            f"{source} • {published}"
        )

        if url:
            st.markdown(
                f"[🔗 Read article]({url})"
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


# ============================================================
# USER QUESTION
# ============================================================

question = st.text_input(
    "🔎 Ask your question",
    placeholder=(
        "Example: What are the biggest risks and benefits "
        "of AI for jobs?"
    ),
)


# ============================================================
# MAIN PIPELINE
# ============================================================

if question:

    question = question.strip()

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    # --------------------------------------------------------
    # WEATHER PIPELINE
    # --------------------------------------------------------

    if is_weather_question(question):

        show_weather(question)

        # Weather questions should not trigger the news pipeline.
        st.stop()

    # --------------------------------------------------------
    # NEWS SEARCH QUERY
    # --------------------------------------------------------

    search_query = build_news_search_query(
        question=question,
        location=news_location,
        topic=topic,
    )

    if not search_query:
        st.warning(
            "I couldn't create a useful news search query "
            "from your question. Try adding a few specific keywords."
        )
        st.stop()

    # Show the query being used for transparency.
    st.markdown(
        f"""
        <div class="search-query">
        🔎 <strong>News search:</strong> {search_query}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FETCH NEWS
    # --------------------------------------------------------

    all_articles = []

    newsdata_error = None
    gnews_error = None

    # NewsData
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

    except Exception as e:

        newsdata_error = str(e)

    # GNews
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

    except Exception as e:

        gnews_error = str(e)

    # --------------------------------------------------------
    # CHECK API RESULTS
    # --------------------------------------------------------

    if not all_articles:

        st.error(
            "No news articles were retrieved."
        )

        if newsdata_error:
            st.warning(
                f"NewsData: {newsdata_error}"
            )

        if gnews_error:
            st.warning(
                f"GNews: {gnews_error}"
            )

        st.info(
            "Try a shorter search-oriented question such as "
            "“AI impact on jobs”."
        )

        st.stop()

    # --------------------------------------------------------
    # RETRIEVE / DEDUPLICATE / RANK
    # --------------------------------------------------------

    relevant_articles = retrieve_articles(
        all_articles,
        question,
        max_articles=article_limit,
    )

    if not relevant_articles:

        st.error(
            "News articles were retrieved, but none were "
            "relevant enough to analyze."
        )
        st.stop()

    st.success(
        f"Retrieved {len(relevant_articles)} relevant articles."
    )

    # --------------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------------

    try:

        if answer_mode == "⚡ Smart Concise Intelligence":

            intelligence = generate_intelligence(
                question=question,
                articles=relevant_articles,
                concise=True,
            )

        elif answer_mode == "📄 Detailed Intelligence Report":

            intelligence = generate_intelligence(
                question=question,
                articles=relevant_articles,
                concise=False,
            )

        else:

            intelligence = generate_advanced_research(
                question=question,
                articles=relevant_articles,
                location=news_location,
                topic=topic,
            )

    except Exception as e:

        st.error(
            f"AI analysis failed: {e}"
        )
        st.stop()

    # --------------------------------------------------------
    # INTELLIGENCE RESULT
    # --------------------------------------------------------

    st.subheader("🧠 Intelligence")

    st.markdown(intelligence)

    # --------------------------------------------------------
    # VISUALIZATIONS
    # --------------------------------------------------------

    try:

        visualizations = generate_visualizations(
            relevant_articles,
            question,
        )

        if visualizations:

            st.subheader("📊 Visual Intelligence")

            render_visualizations_in_streamlit(
                visualizations
            )

    except Exception as e:

        st.warning(
            f"Visualizations could not be generated: {e}"
        )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    render_sources(relevant_articles)
