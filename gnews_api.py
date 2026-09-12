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
        params["q"] = query

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

    for article in data.get("articles", []):

        source = article.get("source") or {}

        normalized_article = {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "source": source.get("name"),
            "published": article.get("publishedAt"),
            "image": article.get("image"),
        }

        articles.append(normalized_article)

    return articles
