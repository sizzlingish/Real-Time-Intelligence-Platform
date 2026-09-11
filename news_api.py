```python
import requests
import streamlit as st


NEWSDATA_API_URL = "https://newsdata.io/api/1/latest"


def get_newsdata_api_key():
    try:
        return st.secrets["NEWSDATA_API_KEY"]
    except KeyError:
        raise ValueError(
            "NEWSDATA_API_KEY is not configured in Streamlit Secrets."
        )


def fetch_news(
    query=None,
    language="en",
    country=None,
    limit=10
):
    api_key = get_newsdata_api_key()

    params = {
        "apikey": api_key,
        "language": language,
    }

    if query:
        params["q"] = query

    if country:
        params["country"] = country

    try:
        response = requests.get(
            NEWSDATA_API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"News API request failed: {e}"
        )

    if data.get("status") != "success":
        raise RuntimeError(
            f"NewsData API error: {data}"
        )

    results = data.get("results", [])

    articles = []

    for article in results[:limit]:

        normalized_article = {
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("link"),
            "source": article.get("source_name"),
            "published": article.get("pubDate"),
            "image": article.get("image_url"),
        }

        articles.append(normalized_article)

    return articles
```
