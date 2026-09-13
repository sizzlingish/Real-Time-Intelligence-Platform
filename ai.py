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
# STANDARD INTELLIGENCE
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

The user may ask simple questions, current
news questions, factual questions, or short
explanatory questions.

USER QUESTION:
{question}

NEWS DATA:
{news_context}


STRICT CONCISE MODE

Answer the user's question using ONLY the
supplied news articles as factual evidence.

OUTPUT REQUIREMENTS:

- Write EXACTLY 3 or 4 short lines.
- Maximum 70 words total.
- Directly answer the user's question.
- Prioritize the newest relevant development.
- Include only the most important information.
- Each line must contain useful information.
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

The user may ask:

- Simple questions
- Difficult questions
- Challenging analytical questions
- Long descriptive questions
- Comparison questions
- "Why" questions
- "How" questions
- University-level research questions

The user asked:

"{question}"

You have been given recent news articles
retrieved from multiple news sources.

Your job is to analyze the supplied articles
and answer the user's question clearly,
factually, and intelligently.

================ NEWS DATA ================

{news_context}

============== END NEWS DATA ==============


IMPORTANT RULES:

1. Use the supplied news articles as your
   primary factual evidence.

2. Do not invent facts.

3. Do not invent names, dates, statistics,
   quotes, locations, organizations, events,
   sources, or URLs.

4. If the sources disagree, clearly identify
   the disagreement.

5. If the available articles are insufficient
   to answer something confidently, say so.

6. Prefer the newest relevant information.

7. Distinguish reported facts from analysis
   and interpretation.

8. Keep the answer useful and well structured.

9. Do not repeat the same information.

10. Do not claim that you personally verified
    information outside the supplied articles.

11. For analytical questions, explain the
    reasoning using evidence from the articles.

12. For "why" questions, explain the relevant
    causes or contributing factors.

13. For "how" questions, explain the process
    step by step when appropriate.

14. For comparison questions, compare the
    relevant subjects using clearly defined
    dimensions.

15. For university-level questions, use an
    academic but easy-to-understand style.

16. Do not present speculation as established
    fact.

17. Future implications must be described as
    possible outcomes rather than certain facts.

18. Real-world examples should only be included
    when supported by the supplied articles.


FORMAT:

### 📰 Intelligence Summary

Give a clear and direct answer to the user's
question.

### 🔎 Key Developments

Explain the most important developments
supported by the retrieved articles.

### ⚖️ Source Comparison

Explain what the sources agree on.

If they disagree, explain the disagreement
and identify the uncertainty.

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

    if concise:

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

        lines = lines[:4]

        words = " ".join(lines).split()

        if len(words) > 70:

            words = words[:70]

            shortened = " ".join(words)

            last_period = shortened.rfind(".")

            if last_period > 30:

                shortened = shortened[
                    :last_period + 1
                ]

            answer = shortened

        else:

            answer = "\n".join(lines)


    return answer


# =========================================================
# ADVANCED RESEARCH / CHALLENGING ANSWER
# =========================================================

def generate_advanced_research(
    question,
    articles,
    location="Worldwide",
    topic="General",
):
    """
    Generate difficult, challenging, analytical,
    comparative, explanatory, and descriptive
    research answers using retrieved news articles.
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
You are an expert research analyst,
intelligence analyst, and academic writer
for the Real-Time Intelligence Platform (RTIP).

USER LOCATION:
{location}

TOPIC:
{topic}

RESEARCH QUESTION:
{question}


==================================================
USER QUESTION TYPE
==================================================

The user may ask:

- Simple questions
- Difficult questions
- Challenging analytical questions
- Long descriptive questions
- Comparison questions
- "Why" questions
- "How" questions
- Cause-and-effect questions
- University-level research questions
- Questions requiring multiple perspectives
- Questions requiring critical analysis
- Questions requiring background and context


==================================================
YOUR TASK
==================================================

Prepare a comprehensive, accurate, balanced,
and well-structured answer to the user's exact
question.

Use the supplied news articles as factual
evidence.

The answer should be detailed enough for a
university-level reader while remaining clear
and easy to understand.

Do not simply summarize the articles.

Analyze the information and explain how the
reported developments relate to the user's
question.


==================================================
STRUCTURE
==================================================

Use the following structure when relevant.

Do not force sections that are not applicable
to the question.


## Direct Answer

Answer the user's question directly before
providing detailed analysis.


## Introduction

Introduce the topic and explain why the
question is important.


## Background and Context

Explain the necessary background needed to
understand the issue.

Define important concepts when necessary.


## Detailed Explanation

Explain difficult concepts step by step in
simple, clear language.

For "how" questions, explain the relevant
processes logically.

For complex questions, break the explanation
into understandable parts.


## Causes and Contributing Factors

Explain the main causes, drivers, conditions,
or factors contributing to the issue.

Distinguish between directly reported causes
and analytical interpretation.


## Effects and Consequences

Explain relevant:

- Short-term effects
- Long-term effects
- Political effects
- Economic effects
- Social effects
- Technological effects
- Environmental effects

Only include dimensions that are relevant to
the question and supported by the evidence.


## Evidence from Recent News

Connect the analysis directly to the supplied
news articles.

Identify which developments support the
analysis.

Mention article sources and publication dates
when available.


## Different Perspectives

Explain relevant perspectives, viewpoints,
stakeholder positions, or disagreements.

Do not manufacture viewpoints that are not
supported by the supplied articles.


## Comparison

If the question involves comparison, clearly
compare the relevant subjects.

Useful comparison dimensions may include:

- Similarities
- Differences
- Advantages
- Disadvantages
- Impact
- Scale
- Risks
- Opportunities
- Short-term outcomes
- Long-term outcomes

Only use dimensions relevant to the question.


## Critical Analysis

Critically evaluate the available evidence.

Discuss:

- Strength of the available evidence
- Important limitations
- Uncertainty
- Conflicting reports
- Missing information
- Alternative interpretations
- What can and cannot be concluded


## Advantages and Disadvantages

When relevant, explain the major advantages
and disadvantages associated with the issue.

Do not include this section when it does not
meaningfully apply.


## Real-World Examples

Provide real-world examples only when they
are supported by the supplied articles.

Do not invent examples.


## Future Implications

Discuss possible future developments based
on the available evidence.

Clearly distinguish possible outcomes from
confirmed facts.

Do not present predictions as certain.


## Conclusion

Provide a balanced, well-structured conclusion
that directly answers the original question.

Summarize the most important findings without
simply repeating the entire answer.


## Sources

List the relevant supplied articles.

For each source, include when available:

- Article title
- Publisher/source
- Publication date
- Original URL

Use only URLs supplied in the news articles.

Do not create fake URLs.


==================================================
FACTUAL ACCURACY RULES
==================================================

1. Use ONLY the supplied articles as factual
   evidence.

2. Do not invent facts.

3. Do not invent statistics.

4. Do not invent names.

5. Do not invent dates.

6. Do not invent quotes.

7. Do not invent organizations.

8. Do not invent events.

9. Do not invent sources.

10. Do not create fake URLs.

11. Clearly identify conflicting information.

12. Clearly identify incomplete information.

13. Separate reported facts from analysis.

14. Do not present assumptions as facts.

15. Do not present predictions as certain.

16. If the articles do not contain enough
    information to answer a particular part
    confidently, explicitly say so.

17. Prefer newer relevant information when
    multiple articles discuss the same issue.

18. Avoid repeating the same evidence in
    multiple sections unless necessary.

19. Answer the exact question asked by the
    user.

20. Do not claim to have independently verified
    information outside the supplied articles.


==================================================
ACADEMIC WRITING STYLE
==================================================

Use:

- Clear explanations
- Logical reasoning
- Evidence-based analysis
- Balanced language
- Appropriate headings
- Short and readable paragraphs
- Bullet points where useful
- University-level analytical depth

Avoid:

- Unsupported claims
- Excessive jargon
- Repetition
- Sensationalism
- Fake certainty
- Personal opinions presented as facts


==================================================
NEWS ARTICLES
==================================================

{news_context}

==================================================
END NEWS ARTICLES
==================================================

Now produce the comprehensive research answer.
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
            f"Gemini Advanced Research request failed: {error}"
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
            "Gemini returned an empty Advanced Research response."
        )

    return answer.strip()
