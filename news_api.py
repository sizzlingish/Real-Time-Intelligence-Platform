import os
import requests


# --------------------------------------------------
# Configuration
# --------------------------------------------------

NEWSDATA_API_URL = "https://newsdata.io/api/1/latest"


# --------------------------------------------------
# Get API Key
# --------------------------------------------------

def get_newsdata_api_key():
    """
    Get the NewsData.io API key from environment variables.
    """

    api_key = os.getenv("NEWSDATA_API_KEY")

    if not api_key:
        raise ValueError(
            "NEWSDATA_API_KEY is not set."
        )

    return api_key


# --------------------------------------------------
# Fetch News
# --------------------------------------------------

def fetch_news(
    query=None,
    language="en",
    country=None,
    limit=10
):
    """
    Fetch latest news from NewsData.io.

    Parameters:
        query    : Search term, e.g. "Pakistan"
        language : News language
        country  : Country code, e.g. "pk"
        limit    : Maximum number of articles

    Returns:
        List of normalized news articles.
    """

    api_key = get_newsdata_api_key()

    params = {
        "apikey": api_key,
        "language": language,
    }

    # Add search query if provided
    if query:
        params["q"] = query

    # Add country if provided
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

    # Check API response
    if data.get("status") != "success":

        raise RuntimeError(
            f"NewsData API error: {data}"
        )

    results = data.get("results", [])

    # --------------------------------------------------
    # Normalize Articles
    # --------------------------------------------------

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


# --------------------------------------------------
# Simple Test
# --------------------------------------------------

if __name__ == "__main__":

    try:

        articles = fetch_news(
            query="Pakistan",
            language="en",
            limit=5
        )

        print("\nLatest News:\n")

        for i, article in enumerate(articles, start=1):

            print(f"{i}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Published: {article['published']}")
            print(f"   URL: {article['url']}")
            print()

    except Exception as e:

        print(f"Error: {e}")
