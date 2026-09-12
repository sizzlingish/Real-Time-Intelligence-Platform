import os

from google import genai


# ---------------------------------------------------------
# GEMINI CONFIGURATION
# ---------------------------------------------------------

MODEL_NAME = "gemini-2.5-flash"


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


def get_client():
    """
    Create and return the Gemini client.
    """

    api_key = get_gemini_api_key()

    return genai.Client(
        api_key=api_key
    )


# ---------------------------------------------------------
# BUILD NEWS CONTEXT
# ---------------------------------------------------------

def build_news_context(articles):
    """
    Convert retrieved news articles into a clean
    text context for Gemini.
    """

    if not articles:
        return "No news articles were found."

    context = []

    for i, article in enumerate(
        articles,
        start=1
    ):

        title = article.get(
            "title",
            "No title available"
        )

        description = article.get(
            "description",
            "No description available"
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
            "url",
            "No URL available"
        )


        article_text = f"""
ARTICLE {i}

Title: {title}

Source: {source}

Published: {published}

Description: {description}

URL: {url}
"""


        context.append(
            article_text.strip()
        )


    return "\n\n".join(context)


# ---------------------------------------------------------
# GENERATE INTELLIGENCE
# ---------------------------------------------------------

def generate_intelligence(
    question,
    articles
):
    """
    Generate an intelligence answer using
    the retrieved news articles.

    Expected usage:

        generate_intelligence(
            question,
            relevant_articles
        )
    """

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    if not articles:
        raise ValueError(
            "No articles were provided."
        )


    client = get_client()

    news_context = build_news_context(
        articles
    )


    prompt = f"""
You are the AI intelligence analyst for
the Real-Time Intelligence Platform (RTIP).

The user asked:

"{question}"


Your task is to answer the user's question
using ONLY the news information provided below.

================ NEWS DATA ================

{news_context}

============== END NEWS DATA ==============


IMPORTANT RULES:

1. Do not invent facts.

2. Do not use information that is not present
   in the supplied news articles.

3. If the articles do not contain enough
   information to answer the question,
   clearly say that the available information
   is insufficient.

4. If different sources report different
   information, identify the disagreement.

5. Distinguish confirmed information from
   uncertainty.

6. Prefer the newest information when discussing
   current developments.

7. Do not repeat the same information unnecessarily.

8. Keep the answer concise and useful.

9. Do not mention that you are an AI unless
   necessary.

10. Do not fabricate statistics, dates, names,
    locations, quotes, or events.


FORMAT YOUR RESPONSE:

### 📰 Intelligence Summary

Give a concise answer to the user's question
based on the retrieved news.


### 🔎 Key Developments

List the most important developments.

Use short bullet points.


### ⚖️ Source Comparison

Explain what the available sources agree on.

If sources disagree, clearly explain the
difference.


### 📌 Why It Matters

Explain why the developments are important,
but only when the significance can reasonably
be supported by the supplied information.


### 🕐 Latest Information

Identify the newest relevant information
available in the retrieved articles.

Mention the source and date when available.


Keep the overall response concise.

Do not add information that is not supported
by the supplied news.
"""


    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

    except Exception as e:

        raise RuntimeError(
            f"Gemini API request failed: {e}"
        ) from e


    if not response:
        raise RuntimeError(
            "Gemini returned an empty response."
        )


    answer = getattr(
        response,
        "text",
        None
    )


    if not answer:
        raise RuntimeError(
            "Gemini returned an empty text response."
        )


    return answer.strip()

