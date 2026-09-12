import os

from google import genai


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# API KEY
# =========================================================

def get_gemini_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set."
        )

    return api_key


# =========================================================
# GEMINI CLIENT
# =========================================================

def get_client():
    api_key = get_gemini_api_key()

    return genai.Client(
        api_key=api_key
    )


# =========================================================
# BUILD NEWS CONTEXT
# =========================================================

def build_news_context(articles):

    if not articles:
        return "No news articles were found."

    context = []

    for index, article in enumerate(
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
ARTICLE {index}

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


# =========================================================
# GENERATE INTELLIGENCE
# =========================================================

def generate_intelligence(
    question,
    articles,
    concise=False
):

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


    # =====================================================
    # CONCISE MODE
    # =====================================================

    if concise:

        prompt = f"""
You are the AI intelligence analyst for RTIP.

User question:
"{question}"

Use ONLY the supplied news articles.

NEWS DATA:
{news_context}

STRICT CONCISE MODE:

Answer in EXACTLY 3 or 4 short lines.

Rules:
- Directly answer the user's question.
- Include only the most important information.
- Mention the latest development if relevant.
- Do not use headings.
- Do not use bullet points.
- Do not explain background.
- Do not add "Why It Matters".
- Do not add a source comparison section.
- Do not repeat information.
- Do not write more than 4 lines.
- Do not exceed 70 words.
- Do not invent facts.

Return ONLY the 3-4 line answer.
"""

================ NEWS DATA ================

{news_context}

============== END NEWS DATA ==============


IMPORTANT RULES:

1. Answer the user's question directly.

2. Use only information supported by the
   supplied articles.

3. Do not invent facts, names, dates,
   statistics, quotes, or events.

4. If sources disagree, briefly mention
   the disagreement.

5. Prefer the newest relevant information.

6. Do not repeat information.

7. Do not add unnecessary background.

8. Keep the answer VERY SHORT.

9. Do not write a long report.

10. Do not include a separate "Why It Matters"
    or "Latest Information" section.


FORMAT:

### 📰 Intelligence Summary

Write 2-3 short sentences directly answering
the user's question.


### 🔎 Key Developments

Give ONLY the 3 most important developments.

Each bullet must be one short sentence.


### ⚖️ Sources

In 1 short sentence, state whether the sources
generally agree or highlight an important
difference.

Keep the entire response concise.
Aim for roughly 100-150 words maximum.
"""

    # =====================================================
    # DETAILED MODE
    # =====================================================

    else:

        prompt = f"""
You are the AI intelligence analyst for
the Real-Time Intelligence Platform (RTIP).

The user asked:

"{question}"

You have been given a collection of recent
news articles retrieved from multiple news
sources.

Your job is to analyze these articles and
answer the user's question.

================ NEWS DATA ================

{news_context}

============== END NEWS DATA ==============


IMPORTANT RULES:

1. Use the supplied news articles as your
   primary evidence.

2. Do not invent facts.

3. Do not invent names, dates, statistics,
   quotes, locations, or events.

4. If the sources disagree, clearly identify
   the disagreement.

5. If the available articles are insufficient
   to answer something confidently, say so.

6. Prefer the newest relevant information.

7. Distinguish reported facts from uncertainty.

8. Keep the answer useful and well structured.

9. Do not repeat the same information.

10. Do not claim that you personally verified
    information outside the supplied articles.


FORMAT:


### 📰 Intelligence Summary

Give a clear answer to the user's question.


### 🔎 Key Developments

Give the most important developments as
short bullet points.


### ⚖️ Source Comparison

Explain what the sources agree on.

If they disagree, explain how.


### 📌 Why It Matters

Explain the significance of the developments
when supported by the available information.


### 🕐 Latest Information

Mention the newest relevant information
available in the supplied articles.

Include the source and publication date
when available.


Keep the response clear, factual, and useful.
"""


    # =====================================================
    # GEMINI REQUEST
    # =====================================================

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

    except Exception as error:

        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error


    # =====================================================
    # VALIDATE RESPONSE
    # =====================================================

    if response is None:

        raise RuntimeError(
            "Gemini returned no response."
        )


    answer = getattr(
        response,
        "text",
        None
    )


    if not answer:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return answer.strip()

