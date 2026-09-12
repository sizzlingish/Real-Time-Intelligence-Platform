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
You are the AI intelligence analyst for
the Real-Time Intelligence Platform (RTIP).

USER QUESTION:
{question}

NEWS DATA:
{news_context}


STRICT CONCISE MODE

Your task is to answer the user's question
using ONLY the supplied news articles.

OUTPUT REQUIREMENTS:

- Write EXACTLY 3 or 4 short lines.
- Maximum 70 words total.
- Directly answer the user's question.
- Include only the most important information.
- Prioritize the newest relevant development.
- Each line should contain useful information.
- Do NOT use headings.
- Do NOT use bullet points.
- Do NOT use numbered lists.
- Do NOT add a "Why It Matters" section.
- Do NOT add a "Source Comparison" section.
- Do NOT add a "Latest Information" section.
- Do NOT repeat information.
- Do NOT add an introduction or conclusion.
- Do NOT mention these instructions.
- Do NOT invent facts.

If the sources disagree, mention the
disagreement briefly within one of the lines.

Return ONLY the 3-4 lines of the answer.
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


    answer = answer.strip()


    # =====================================================
    # FINAL CONCISE CLEANUP
    # =====================================================
    #
    # This provides an additional safeguard in case
    # Gemini ignores the length instruction.
    #

    if concise:

        # Remove markdown headings/bullets if Gemini
        # accidentally adds them.

        lines = []

        for line in answer.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith("- "):
                line = line[2:].strip()

            if line.startswith("* "):
                line = line[2:].strip()

            if line:
                lines.append(line)


        # Keep only the first 4 useful lines.

        lines = lines[:4]


        # If Gemini returned more than 70 words,
        # trim at a word boundary.

        words = " ".join(lines).split()

        if len(words) > 70:

            words = words[:70]

            shortened = " ".join(words)

            # Avoid leaving an obviously unfinished
            # sentence where possible.

            last_period = shortened.rfind(".")

            if last_period > 30:

                shortened = shortened[
                    :last_period + 1
                ]

            answer = shortened

        else:

            answer = "\n".join(lines)


    return answer

