import re
from difflib import SequenceMatcher


# --------------------------------------------------
# Text Cleaning
# --------------------------------------------------

def clean_text(text):
    """
    Clean and normalize text for comparison.
    """

    if not text:
        return ""

    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# Calculate Similarity
# --------------------------------------------------

def similarity(text1, text2):
    """
    Calculate similarity between two pieces of text.
    Returns a value between 0 and 1.
    """

    text1 = clean_text(text1)
    text2 = clean_text(text2)

    if not text1 or not text2:
        return 0

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


# --------------------------------------------------
# Remove Duplicate Articles
# --------------------------------------------------

def remove_duplicates(articles, similarity_threshold=0.85):
    """
    Remove duplicate or highly similar news articles.
    """

    unique_articles = []

    seen_urls = set()

    for article in articles:

        url = article.get("url")
        title = article.get("title", "")

        # ------------------------------------------
        # URL duplicate check
        # ------------------------------------------

        if url and url in seen_urls:
            continue

        # ------------------------------------------
        # Title duplicate check
        # ------------------------------------------

        duplicate = False

        for existing in unique_articles:

            existing_title = existing.get(
                "title",
                ""
            )

            if similarity(
                title,
                existing_title
            ) >= similarity_threshold:

                duplicate = True
                break

        if duplicate:
            continue

        if url:
            seen_urls.add(url)

        unique_articles.append(article)

    return unique_articles


# --------------------------------------------------
# Calculate Relevance
# --------------------------------------------------

def calculate_relevance(article, question):
    """
    Calculate a simple relevance score based on
    keywords appearing in the user's question.
    """

    question_words = set(
        clean_text(question).split()
    )

    if not question_words:
        return 0

    title = clean_text(
        article.get("title", "")
    )

    description = clean_text(
        article.get("description", "")
    )

    article_text = (
        title + " " + description
    )

    article_words = set(
        article_text.split()
    )

    # Count matching words
    matches = question_words.intersection(
        article_words
    )

    return len(matches)


# --------------------------------------------------
# Rank Articles
# --------------------------------------------------

def rank_articles(articles, question):
    """
    Rank articles according to their relevance
    to the user's question.
    """

    ranked_articles = []

    for article in articles:

        score = calculate_relevance(
            article,
            question
        )

        article_copy = article.copy()

        article_copy["relevance_score"] = score

        ranked_articles.append(
            article_copy
        )

    # Highest relevance first
    ranked_articles.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    return ranked_articles


# --------------------------------------------------
# Retrieve Relevant Articles
# --------------------------------------------------

def retrieve_articles(
    articles,
    question,
    max_articles=8
):
    """
    Complete retrieval pipeline.

    Steps:
    1. Remove invalid articles
    2. Remove duplicates
    3. Rank by relevance
    4. Return top articles
    """

    if not articles:
        return []

    # ------------------------------------------
    # Remove articles without titles
    # ------------------------------------------

    valid_articles = [
        article
        for article in articles
        if article.get("title")
    ]

    # ------------------------------------------
    # Remove duplicates
    # ------------------------------------------

    unique_articles = remove_duplicates(
        valid_articles
    )

    # ------------------------------------------
    # Rank articles
    # ------------------------------------------

    ranked_articles = rank_articles(
        unique_articles,
        question
    )

    # ------------------------------------------
    # Select top articles
    # ------------------------------------------

    selected_articles = ranked_articles[
        :max_articles
    ]

    return selected_articles


# --------------------------------------------------
# Simple Test
# --------------------------------------------------

if __name__ == "__main__":

    test_articles = [

        {
            "title": "Pakistan announces new economic policy",
            "description": "Government announces changes to the economy.",
            "url": "https://example.com/1",
            "source": "News Source A",
            "published": "2026-09-12"
        },

        {
            "title": "Pakistan announces new economic policy",
            "description": "Government announces economic changes.",
            "url": "https://example.com/2",
            "source": "News Source B",
            "published": "2026-09-12"
        },

        {
            "title": "Pakistan cricket team wins match",
            "description": "Pakistan wins an important cricket match.",
            "url": "https://example.com/3",
            "source": "Sports News",
            "published": "2026-09-12"
        }
    ]

    question = "What is happening with Pakistan's economy?"

    results = retrieve_articles(
        test_articles,
        question,
        max_articles=5
    )

    print("\nRetrieved Articles:\n")

    for article in results:

        print(
            f"Title: {article['title']}"
        )

        print(
            f"Relevance: "
            f"{article.get('relevance_score', 0)}"
        )

        print(
            f"Source: {article.get('source')}"
        )

        print()
