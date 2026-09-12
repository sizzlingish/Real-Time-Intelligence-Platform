import re
import requests
import streamlit as st


GNEWS_API_URL = "https://gnews.io/api/v4/search"


def get_gnews_api_key():
    try:
        return st.secrets["GNEWS_API_KEY"]
    except KeyError:
        raise ValueError(
            "GNEWS_API_KEY is not configured in Streamlit Secrets."
        )


def clean_gnews_query(query):
    """
    Clean the user's question before sending it to GNews.
    Removes emojis and characters that can cause
    GNews query syntax errors.
    """

    if not query:
        return ""

    # Remove emojis / non-standard characters
    query = query.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    # Remove punctuation that can cause query issues
    query = re.sub(
        r"[^\w\s-]",
        " ",
        query
    )

    # Remove excessive whitespace
    query = re.sub(
        r"\s+",
        " ",
        query
    ).strip()

    return query


def fetch_gnews(
    query=None,
    language="en",
    country=None,
    max_results=10
):

    api_key = get_gnews_api_key()

    params = {
        "apikey": api_key,
        "lang": language,
        "max": max_results,
        "sortby": "publishedAt",
    }

    if query:

        clean_query = clean_gnews_query(
            query
        )

        if clean_query:

            params["q"] = clean_query

    if country:

        params["country"] = country

    try:

        response = requests.get(
            GNEWS_API_URL,
            params=params,
            timeout=15
        )

        if response.status_code != 200:

            raise RuntimeError(
                f"GNews API error: "
                f"{response.status_code} - "
                f"{response.text}"
            )

        data = response.json()

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"GNews API request failed: {e}"
        )

    if "articles" not in data:

        raise RuntimeError(
            f"GNews API error: {data}"
        )

    articles = []

    for article in data.get(
        "articles",
        []
    ):

        source = (
            article.get("source")
            or {}
        )

        normalized_article = {

            "title": article.get(
                "title"
            ),

            "description": article.get(
                "description"
            ),

            "url": article.get(
                "url"
            ),

            "source": source.get(
                "name"
            ),

            "published": article.get(
                "publishedAt"
            ),

            "image": article.get(
                "image"
            ),
        }

        articles.append(
            normalized_article
        )

    return articles
