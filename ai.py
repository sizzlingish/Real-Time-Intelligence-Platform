import os
from google import genai


# --------------------------------------------------
# Configuration
# --------------------------------------------------

def get_gemini_api_key():
    """
    Get the Gemini API key from environment variables.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set."
        )

    return api_key


# --------------------------------------------------
# Create Gemini Client
# --------------------------------------------------

def get_client():
    """
    Create and return the Gemini client.
    """

    api_key = get_gemini_api_key()

    return genai.Client(
        api_key=api_key
    )


# --------------------------------------------------
# Build News Context
# --------------------------------------------------

def build_news_context(articles):
    """
    Convert retrieved news articles into text
    that Gemini can analyze.
    """

    if not articles:
        return "No news articles were found."

    context = []

    for i, article in enumerate(articles, start=1):

        title = article.get("title", "No title")
        description = article.get(
            "description",
            "No description available."
        )
        source = article.get(
            "source",
            "Unknown source"
        )
        published = article.get(
            "published",
            "Unknown time"
        )
        url = article.get(
            "url",
            "No URL"
        )

        article_text = f"""
ARTICLE {i}

Title: {title}
Source: {source}
Published: {published}
Description: {description}
URL: {url}
"""

        context.append(article_text)

    return "\n".join(context)


# --------------------------------------------------
# Generate Intelligence
# --------------------------------------------------

def generate_intelligence(question, articles):
    """
    Generate an AI-powered intelligence response
    using the retrieved news articles.
    """

    client = get_client()

    news_context = build_news_context(articles)

    prompt = f"""
You are the AI analyst for the
Real-Time Intelligence Platform (RTIP).

The user has asked:

"{question}"

Below are current news articles retrieved from
external news sources.

---------------- NEWS DATA ----------------

{news_context}

-------------- END NEWS DATA --------------

Your job is to analyze ONLY the information
provided in the news data.

Do NOT invent facts.

If the available information is insufficient,
clearly say so.

If different sources report conflicting
information, identify the disagreement.

Structure your response using these sections:

### 📰 Intelligence Summary
Give a concise summary of what is happening.

### 🔎 Key Developments
List the most important developments.

### ⚖️ Source Comparison
Explain what the available sources agree on
and where they differ.

### 📌 Why It Matters
Explain the significance or possible impact
based only on the available information.

### 🕐 Latest Information
Mention the most recent information available
from the supplied articles.

Keep the response clear, factual and concise.

Do not present speculation as fact.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        raise RuntimeError(
            f"Gemini API request failed: {e}"
        )


# --------------------------------------------------
# Simple Test
# --------------------------------------------------

if __name__ == "__main__":

    test_articles = [
        {
            "title": "Example news headline",
            "description": (
                "Example description of a current event."
            ),
            "url": "https://example.com",
            "source": "Example News",
            "published": "2026-09-12 10:00:00",
        }
    ]

    question = "What is happening in this story?"

    try:

        answer = generate_intelligence(
            question,
            test_articles
        )

        print("\nRTIP Intelligence:\n")
        print(answer)

    except Exception as e:

        print(f"Error: {e}")
