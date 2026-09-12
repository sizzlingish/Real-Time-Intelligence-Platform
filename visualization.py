"""
visualization.py

Dynamic Graph Generation System for the
Real-Time Intelligence Platform (RTIP).

This module decides which visualizations are worth generating
from retrieved articles/events based on the user's question
and the available data.
"""

import re
from datetime import datetime, timedelta
from collections import Counter


# ==================================================
# Date Parsing
# ==================================================

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%d",
    "%d %b %Y",
    "%B %d, %Y",
]


def parse_date(value):
    """
    Best-effort parsing of a date/time string.

    Returns None if parsing fails.
    """

    if not value:
        return None

    if isinstance(value, datetime):
        return value

    value = str(value).strip()

    for fmt in DATE_FORMATS:

        try:
            return datetime.strptime(
                value,
                fmt
            )

        except ValueError:
            continue

    match = re.match(
        r"(\d{4}-\d{2}-\d{2})",
        value
    )

    if match:

        try:
            return datetime.strptime(
                match.group(1),
                "%Y-%m-%d"
            )

        except ValueError:
            return None

    return None


# ==================================================
# STEP 1: Analyze Data
# ==================================================

def analyze_data(data):

    profile = {

        "count": len(data or []),

        "has_dates": False,
        "date_count": 0,
        "date_range_days": 0,
        "earliest_date": None,
        "latest_date": None,

        "has_relevance_scores": False,
        "relevance_count": 0,

        "has_sources": False,
        "unique_sources": 0,

        "has_locations": False,
        "unique_locations": 0,

        "has_categories": False,
        "unique_categories": 0,

        "has_entities": False,
        "unique_entities": 0,
        "entity_pairs": 0,
    }

    if not data:
        return profile

    dates = []
    sources = set()
    locations = set()
    categories = set()
    entities = Counter()

    entity_pairs = 0
    relevance_values = []

    for item in data:

        # ------------------------------
        # Dates
        # ------------------------------

        parsed = parse_date(
            item.get("published")
        )

        if parsed:
            dates.append(parsed)

        # ------------------------------
        # Sources
        # ------------------------------

        source = item.get("source")

        if source:
            sources.add(source)

        # ------------------------------
        # Locations
        # ------------------------------

        location = (
            item.get("country")
            or item.get("location")
        )

        if location:
            locations.add(location)

        # ------------------------------
        # Categories
        # ------------------------------

        category = item.get("category")

        if category:
            categories.add(category)

        # ------------------------------
        # Entities
        # ------------------------------

        item_entities = (
            item.get("entities")
            or []
        )

        if item_entities:

            for entity in item_entities:
                entities[entity] += 1

            if len(item_entities) >= 2:
                entity_pairs += 1

        # ------------------------------
        # Relevance
        # ------------------------------

        score = item.get(
            "relevance_score"
        )

        if isinstance(
            score,
            (int, float)
        ):
            relevance_values.append(score)

    # ------------------------------
    # Store profile
    # ------------------------------

    profile["date_count"] = len(dates)

    profile["has_dates"] = (
        len(dates) >= 3
    )

    if dates:

        profile["earliest_date"] = min(dates)
        profile["latest_date"] = max(dates)

        profile["date_range_days"] = (
            profile["latest_date"]
            - profile["earliest_date"]
        ).days

    profile["relevance_count"] = (
        len(relevance_values)
    )

    profile["has_relevance_scores"] = (
        len(relevance_values) >= 3
    )

    profile["unique_sources"] = (
        len(sources)
    )

    profile["has_sources"] = (
        len(sources) >= 2
    )

    profile["unique_locations"] = (
        len(locations)
    )

    profile["has_locations"] = (
        len(locations) >= 2
    )

    profile["unique_categories"] = (
        len(categories)
    )

    profile["has_categories"] = (
        len(categories) >= 2
    )

    profile["unique_entities"] = (
        len(entities)
    )

    profile["has_entities"] = (
        entity_pairs >= 3
    )

    profile["entity_pairs"] = (
        entity_pairs
    )

    return profile


# ==================================================
# STEP 2: Analyze Question
# ==================================================

QUESTION_INTENT_KEYWORDS = {

    "temporal": [
        "over time",
        "timeline",
        "recent",
        "today",
        "this week",
        "this month",
        "last 30 days",
        "changed",
        "chronology",
        "sequence",
        "before",
        "after",
        "develop",
        "since",
        "so far",
        "latest",
        "when",
    ],

    "comparative": [
        "compare",
        "comparison",
        "versus",
        " vs ",
        "difference",
        "which",
        "most",
        "least",
        "highest",
        "lowest",
        "rank",
        "top",
        "worst",
        "best",
    ],

    "geographic": [
        "country",
        "countries",
        "region",
        "city",
        "cities",
        "where",
        "location",
        "area",
        "border",
        "state",
    ],

    "relevance": [
        "relevant",
        "relevance",
        "confidence",
        "reliable",
        "how sure",
        "how accurate",
        "trust",
    ],

    "historical": [
        "historical",
        "history",
        "previously",
        "in the past",
        "used to",
        "compared to last",
        "precedent",
    ],

    "relationship": [
        "relationship",
        "connection",
        "linked",
        "involved",
        "who is behind",
        "network",
        "ties",
        "associated",
    ],
}


def analyze_question(question):

    text = f" {(question or '').lower()} "

    intents = {}

    for intent, keywords in (
        QUESTION_INTENT_KEYWORDS.items()
    ):

        matched = [
            keyword
            for keyword in keywords
            if keyword in text
        ]

        intents[intent] = {
            "matched": bool(matched),
            "matched_keywords": matched,
        }

    # Generic questions get a light default.
    if not any(
        value["matched"]
        for value in intents.values()
    ):

        intents["temporal"]["matched"] = True

        intents["temporal"][
            "matched_keywords"
        ] = ["default"]

        intents["comparative"]["matched"] = True

        intents["comparative"][
            "matched_keywords"
        ] = ["default"]

    return {
        "raw_question": question,
        "intents": intents,
    }


# ==================================================
# STEP 3: Visualization Catalog
# ==================================================

VISUALIZATION_CATALOG = {

    "timeline": {
        "requires": ["has_dates"],
        "intents": [
            "temporal",
            "historical"
        ],
    },

    "event_frequency_by_date": {
        "requires": ["has_dates"],
        "intents": ["temporal"],
    },

    "relevance_distribution": {
        "requires": ["has_relevance_scores"],
        "intents": ["relevance"],
    },

    "relevance_ranking": {
        "requires": ["has_relevance_scores"],
        "intents": [
            "relevance",
            "comparative"
        ],
    },

    "source_comparison": {
        "requires": ["has_sources"],
        "intents": [
            "comparative",
            "relevance"
        ],
    },

    "geographic_distribution": {
        "requires": ["has_locations"],
        "intents": ["geographic"],
    },

    "category_comparison": {
        "requires": ["has_categories"],
        "intents": ["comparative"],
    },

    "historical_comparison": {
        "requires": ["has_dates"],
        "intents": [
            "historical",
            "temporal"
        ],
        "min_range_days": 14,
    },

    "entity_network": {
        "requires": ["has_entities"],
        "intents": ["relationship"],
    },
}


def identify_available_visualizations(
    data_profile
):

    available = []

    for viz_type, spec in (
        VISUALIZATION_CATALOG.items()
    ):

        requirements_met = all(
            data_profile.get(flag)
            for flag in spec["requires"]
        )

        if not requirements_met:
            continue

        if "min_range_days" in spec:

            if (
                data_profile.get(
                    "date_range_days",
                    0
                )
                < spec["min_range_days"]
            ):
                continue

        available.append(viz_type)

    return available


# ==================================================
# STEP 4: Evaluate Relevance
# ==================================================

def evaluate_visualization_relevance(
    visualization,
    question_analysis,
    data_profile
):

    spec = VISUALIZATION_CATALOG[
        visualization
    ]

    intents = question_analysis[
        "intents"
    ]

    matched_intents = [
        intent
        for intent in spec["intents"]
        if intents.get(
            intent,
            {}
        ).get("matched")
    ]

    if not matched_intents:
        return 0.15

    return min(
        1.0,
        0.55 + 0.2 * len(matched_intents)
    )


# ==================================================
# STEP 5: Evaluate Data Sufficiency
# ==================================================

SUFFICIENCY_RULES = {

    "timeline":
        lambda p: p["date_count"] / 6,

    "event_frequency_by_date":
        lambda p: p["date_count"] / 6,

    "relevance_distribution":
        lambda p: p["relevance_count"] / 8,

    "relevance_ranking":
        lambda p: p["relevance_count"] / 5,

    "source_comparison":
        lambda p: p["unique_sources"] / 3,

    "geographic_distribution":
        lambda p: p["unique_locations"] / 3,

    "category_comparison":
        lambda p: p["unique_categories"] / 3,

    "historical_comparison":
        lambda p: p["date_range_days"] / 30,

    "entity_network":
        lambda p: p["entity_pairs"] / 6,
}


def evaluate_data_sufficiency(
    visualization,
    data_profile
):

    rule = SUFFICIENCY_RULES.get(
        visualization
    )

    if not rule:
        return 0.0

    try:

        return max(
            0.0,
            min(
                1.0,
                rule(data_profile)
            )
        )

    except ZeroDivisionError:

        return 0.0


# ==================================================
# STEP 6: Rank Visualizations
# ==================================================

REDUNDANCY_GROUPS = [

    {
        "timeline",
        "event_frequency_by_date"
    },

    {
        "relevance_distribution",
        "relevance_ranking"
    },
]


def rank_visualizations(
    candidates,
    question_analysis,
    data_profile
):

    ranked = []

    for viz in candidates:

        relevance = (
            evaluate_visualization_relevance(
                viz,
                question_analysis,
                data_profile
            )
        )

        sufficiency = (
            evaluate_data_sufficiency(
                viz,
                data_profile
            )
        )

        score = round(
            (relevance * 0.6)
            + (sufficiency * 0.4),
            3
        )

        reason = _explain_score(
            viz,
            relevance,
            sufficiency,
            question_analysis
        )

        ranked.append({
            "type": viz,
            "score": score,
            "relevance": round(
                relevance,
                3
            ),
            "sufficiency": round(
                sufficiency,
                3
            ),
            "reason": reason,
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked


def _explain_score(
    viz,
    relevance,
    sufficiency,
    question_analysis
):

    matched = [
        intent
        for intent, info
        in question_analysis[
            "intents"
        ].items()
        if (
            info.get("matched")
            and intent
            in VISUALIZATION_CATALOG[
                viz
            ]["intents"]
        )
    ]

    if relevance <= 0.15:

        return (
            f"The data supports a '{viz}' chart, "
            f"but the question doesn't ask for "
            f"that kind of insight."
        )

    if sufficiency < 0.4:

        return (
            f"The question relates to "
            f"{', '.join(matched) or 'this topic'}, "
            f"which a '{viz}' chart would help with, "
            f"but there isn't enough reliable data yet "
            f"to make it meaningful."
        )

    return (
        f"The question relates to "
        f"{', '.join(matched) or 'this topic'}, "
        f"and the dataset has enough supporting data "
        f"for a reliable '{viz}' chart."
    )


# ==================================================
# STEP 7: Select Visualizations
# ==================================================

def select_visualizations(
    ranked_visualizations,
    max_graphs=3,
    min_score=0.35
):

    selected = []
    used_groups = []

    for candidate in ranked_visualizations:

        if candidate["score"] < min_score:
            continue

        group = next(
            (
                group
                for group in REDUNDANCY_GROUPS
                if candidate["type"] in group
            ),
            None
        )

        if group and group in used_groups:
            continue

        selected.append(candidate)

        if group:
            used_groups.append(group)

        if len(selected) >= max_graphs:
            break

    return selected


# ==================================================
# STEP 8: Graph Configuration
# ==================================================

def generate_graph_config(
    visualization,
    data
):

    viz_type = visualization[
        "type"
    ]

    builder = _CONFIG_BUILDERS.get(
        viz_type
    )

    if not builder:
        return None

    config = builder(data)

    config.update({
        "type": viz_type,
        "score": visualization[
            "score"
        ],
        "reason": visualization[
            "reason"
        ],
    })

    return config


# ==================================================
# Timeline
# ==================================================

def _build_timeline(data):

    points = []

    for item in data:

        parsed = parse_date(
            item.get("published")
        )

        if parsed:

            points.append({
                "x": parsed.isoformat(),
                "label": item.get(
                    "title",
                    "Untitled"
                ),
                "source": item.get(
                    "source",
                    ""
                ),
            })

    points.sort(
        key=lambda p: p["x"]
    )

    return {
        "chart": "timeline",
        "x_axis": "published",
        "y_axis": "event",
        "points": points,
    }


# ==================================================
# Event Frequency
# ==================================================

def _build_event_frequency_by_date(
    data
):

    counts = Counter()

    for item in data:

        parsed = parse_date(
            item.get("published")
        )

        if parsed:

            counts[
                parsed.date().isoformat()
            ] += 1

    ordered = sorted(
        counts.items()
    )

    return {
        "chart": "line",
        "x_axis": "date",
        "y_axis": "event_count",
        "x": [
            date
            for date, _ in ordered
        ],
        "y": [
            count
            for _, count in ordered
        ],
    }


# ==================================================
# Relevance Distribution
# ==================================================

def _build_relevance_distribution(
    data
):

    values = [

        item.get(
            "relevance_score"
        )

        for item in data

        if isinstance(
            item.get(
                "relevance_score"
            ),
            (int, float)
        )
    ]

    return {
        "chart": "histogram",
        "x_axis": "relevance_score",
        "y_axis": "frequency",
        "values": values,
    }


# ==================================================
# Relevance Ranking
# ==================================================

def _build_relevance_ranking(
    data
):

    ranked = sorted(

        (
            item
            for item in data
            if isinstance(
                item.get(
                    "relevance_score"
                ),
                (int, float)
            )
        ),

        key=lambda item:
            item["relevance_score"],

        reverse=True
    )[:10]

    return {
        "chart": "bar",
        "x_axis": "title",
        "y_axis": "relevance_score",

        "x": [
            item.get(
                "title",
                "Untitled"
            )[:60]

            for item in ranked
        ],

        "y": [
            item[
                "relevance_score"
            ]

            for item in ranked
        ],
    }


# ==================================================
# Source Comparison
# ==================================================

def _build_source_comparison(
    data
):

    counts = Counter(
        item.get("source")
        for item in data
        if item.get("source")
    )

    ordered = counts.most_common()

    return {
        "chart": "bar",
        "x_axis": "source",
        "y_axis": "article_count",

        "x": [
            source
            for source, _ in ordered
        ],

        "y": [
            count
            for _, count in ordered
        ],
    }


# ==================================================
# Geographic Distribution
# ==================================================

def _build_geographic_distribution(
    data
):

    counts = Counter(

        item.get("country")
        or item.get("location")

        for item in data

        if (
            item.get("country")
            or item.get("location")
        )
    )

    ordered = counts.most_common()

    return {
        "chart": (
            "map"
            if len(ordered) > 1
            else "bar"
        ),

        "x_axis": "country",
        "y_axis": "event_count",

        "x": [
            location
            for location, _ in ordered
        ],

        "y": [
            count
            for _, count in ordered
        ],
    }


# ==================================================
# Category Comparison
# ==================================================

def _build_category_comparison(
    data
):

    counts = Counter(
        item.get("category")
        for item in data
        if item.get("category")
    )

    ordered = counts.most_common()

    return {
        "chart": "bar",
        "x_axis": "category",
        "y_axis": "event_count",

        "x": [
            category
            for category, _ in ordered
        ],

        "y": [
            count
            for _, count in ordered
        ],
    }


# ==================================================
# Historical Comparison
# ==================================================

def _build_historical_comparison(
    data
):

    dated = []

    for item in data:

        parsed = parse_date(
            item.get("published")
        )

        if parsed:

            dated.append(
                (
                    parsed,
                    item
                )
            )

    if not dated:

        return {
            "chart": "bar",
            "x_axis": "period",
            "y_axis": "event_count",
            "x": [],
            "y": [],
        }

    dated.sort(
        key=lambda pair: pair[0]
    )

    earliest = dated[0][0]
    latest = dated[-1][0]

    midpoint = (
        latest
        - timedelta(
            days=(
                latest - earliest
            ).days / 2
        )
    )

    recent = sum(
        1
        for date, _ in dated
        if date >= midpoint
    )

    older = sum(
        1
        for date, _ in dated
        if date < midpoint
    )

    return {
        "chart": "bar",
        "x_axis": "period",
        "y_axis": "event_count",

        "x": [
            "Earlier period",
            "Recent period"
        ],

        "y": [
            older,
            recent
        ],
    }


# ==================================================
# Entity Network
# ==================================================

def _build_entity_network(
    data
):

    edges = Counter()

    for item in data:

        entities = (
            item.get("entities")
            or []
        )

        for i in range(
            len(entities)
        ):

            for j in range(
                i + 1,
                len(entities)
            ):

                pair = tuple(
                    sorted(
                        [
                            entities[i],
                            entities[j]
                        ]
                    )
                )

                edges[pair] += 1

    return {
        "chart": "network",
        "x_axis": "entity",
        "y_axis": "entity",

        "edges": [
            {
                "source": source,
                "target": target,
                "weight": weight,
            }

            for (
                source,
                target
            ), weight
            in edges.most_common(30)
        ],
    }


# ==================================================
# Configuration Builders
# ==================================================

_CONFIG_BUILDERS = {

    "timeline":
        _build_timeline,

    "event_frequency_by_date":
        _build_event_frequency_by_date,

    "relevance_distribution":
        _build_relevance_distribution,

    "relevance_ranking":
        _build_relevance_ranking,

    "source_comparison":
        _build_source_comparison,

    "geographic_distribution":
        _build_geographic_distribution,

    "category_comparison":
        _build_category_comparison,

    "historical_comparison":
        _build_historical_comparison,

    "entity_network":
        _build_entity_network,
}


# ==================================================
# STEP 9: Main Visualization Orchestrator
# ==================================================

def generate_visualizations(
    data,
    question,
    scenario=None,
    max_graphs=3
):

    data_profile = analyze_data(
        data
    )

    if data_profile["count"] == 0:

        return {
            "recommended_visualizations": [],
            "message": (
                "No meaningful visualization available: "
                "no data was gathered."
            ),
        }

    question_analysis = (
        analyze_question(question)
    )

    available = (
        identify_available_visualizations(
            data_profile
        )
    )

    if not available:

        return {
            "recommended_visualizations": [],
            "data_profile": data_profile,
            "message": (
                "No meaningful visualization available: "
                "the gathered information doesn't contain "
                "enough structured data to chart."
            ),
        }

    ranked = rank_visualizations(
        available,
        question_analysis,
        data_profile
    )

    selected = select_visualizations(
        ranked,
        max_graphs=max_graphs
    )

    if not selected:

        return {
            "recommended_visualizations": [],
            "data_profile": data_profile,
            "message": (
                "No meaningful visualization available: "
                "candidate graphs did not clear the "
                "relevance/sufficiency bar."
            ),
        }

    results = []

    for priority, candidate in enumerate(
        selected,
        start=1
    ):

        config = generate_graph_config(
            candidate,
            data
        )

        if config:

            config["priority"] = (
                priority
            )

            results.append(config)

    return {
        "recommended_visualizations": results,

        "data_profile": data_profile,

        "question_analysis": {
            "matched_intents": [
                intent

                for intent, info
                in question_analysis[
                    "intents"
                ].items()

                if info["matched"]
            ]
        },
    }


# ==================================================
# STEP 10: Plotly Rendering
# ==================================================

def render_visualization(
    config
):

    import plotly.express as px
    import plotly.graph_objects as go

    chart = config.get(
        "chart"
    )

    # ----------------------------------------------
    # Timeline
    # ----------------------------------------------

    if chart == "timeline":

        points = config.get(
            "points",
            []
        )

        if not points:
            return None

        fig = px.scatter(

            x=[
                point["x"]
                for point in points
            ],

            y=[
                point["label"]
                for point in points
            ],

            hover_name=[
                point.get(
                    "source",
                    ""
                )

                for point in points
            ],

            title="Event Timeline",
        )

        fig.update_yaxes(
            visible=False
        )

        return fig

    # ----------------------------------------------
    # Line Chart
    # ----------------------------------------------

    if chart == "line":

        if not config.get("x"):
            return None

        return px.line(

            x=config.get(
                "x",
                []
            ),

            y=config.get(
                "y",
                []
            ),

            labels={
                "x": config.get(
                    "x_axis"
                ),

                "y": config.get(
                    "y_axis"
                ),
            },

            title=(
                "Event Frequency Over Time"
            ),
        )

    # ----------------------------------------------
    # Histogram
    # ----------------------------------------------

    if chart == "histogram":

        if not config.get("values"):
            return None

        return px.histogram(

            x=config.get(
                "values",
                []
            ),

            labels={
                "x": config.get(
                    "x_axis"
                )
            },

            title=(
                "Relevance Score Distribution"
            ),
        )

    # ----------------------------------------------
    # Bar Chart
    # ----------------------------------------------

    if chart == "bar":

        if not config.get("x"):
            return None

        return px.bar(

            x=config.get(
                "x",
                []
            ),

            y=config.get(
                "y",
                []
            ),

            labels={
                "x": config.get(
                    "x_axis"
                ),

                "y": config.get(
                    "y_axis"
                ),
            },

            title=(
                config.get(
                    "x_axis",
                    ""
                )
                .replace(
                    "_",
                    " "
                )
                .title()
            ),
        )

    # ----------------------------------------------
    # Geographic Distribution
    # ----------------------------------------------

    if chart == "map":

        if not config.get("x"):
            return None

        # A true geographic map would require
        # coordinates or ISO country codes.
        # Until those are available, use a
        # categorical bar chart instead.

        return px.bar(

            x=config.get(
                "x",
                []
            ),

            y=config.get(
                "y",
                []
            ),

            labels={
                "x": "country",
                "y": "event_count"
            },

            title=(
                "Geographic Distribution"
            ),
        )

    # ----------------------------------------------
    # Entity Network
    # ----------------------------------------------

    if chart == "network":

        edges = config.get(
            "edges",
            []
        )

        if not edges:
            return None

        fig = go.Figure()

        for edge in edges:

            fig.add_trace(
                go.Scatter(

                    x=[0, 1],

                    y=[0, 1],

                    mode=(
                        "lines+markers+text"
                    ),

                    text=[
                        edge["source"],
                        edge["target"]
                    ],

                    showlegend=False,
                )
            )

        fig.update_layout(
            title=(
                "Entity Relationship Graph"
            )
        )

        return fig

    return None


# ==================================================
# Streamlit Rendering Helper
# ==================================================

def render_visualizations_in_streamlit(
    result
):

    import streamlit as st

    visualizations = result.get(
        "recommended_visualizations",
        []
    )

    if not visualizations:

        st.info(
            result.get(
                "message",
                "No visualizations available."
            )
        )

        return

    st.subheader(
        "📊 Visual Intelligence"
    )

    for config in visualizations:

        reason = config.get(
            "reason",
            ""
        )

        if reason:
            st.caption(reason)

        fig = render_visualization(
            config
        )

        if fig is not None:

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif config.get(
            "chart"
        ) == "network":

            st.write(
                "Entity relationships:"
            )

            for edge in config.get(
                "edges",
                []
            ):

                st.write(
                    f"- "
                    f"{edge['source']} "
                    f"↔ "
                    f"{edge['target']} "
                    f"({edge['weight']}x)"
                )


# ==================================================
# Simple Test / Demo
# ==================================================

if __name__ == "__main__":

    import json

    test_articles = [

        {
            "title": (
                "Flood warnings issued "
                "across the region"
            ),

            "description": (
                "Authorities warn of "
                "rising water levels."
            ),

            "source": "Reuters",

            "published":
                "2026-09-01 08:00:00",

            "country": "Pakistan",

            "relevance_score": 9,
        },

        {
            "title": (
                "Flooding worsens, "
                "thousands evacuated"
            ),

            "description": (
                "Evacuations continue "
                "as rivers overflow."
            ),

            "source": "BBC",

            "published":
                "2026-09-05 12:30:00",

            "country": "Pakistan",

            "relevance_score": 8,
        },

        {
            "title": (
                "Government announces "
                "relief fund"
            ),

            "description": (
                "New relief package approved "
                "for flood victims."
            ),

            "source": "Al Jazeera",

            "published":
                "2026-09-08 09:15:00",

            "country": "Pakistan",

            "relevance_score": 7,
        },

        {
            "title": (
                "Neighboring region reports "
                "minor flooding"
            ),

            "description": (
                "Lower impact reported nearby."
            ),

            "source": "Reuters",

            "published":
                "2026-09-09 14:00:00",

            "country": "India",

            "relevance_score": 4,
        },

        {
            "title": (
                "Death toll rises as rescue "
                "efforts continue"
            ),

            "description": (
                "Officials update casualty figures."
            ),

            "source": "BBC",

            "published":
                "2026-09-11 07:45:00",

            "country": "Pakistan",

            "relevance_score": 9,
        },

        {
            "title": (
                "Relief supplies reach "
                "affected areas"
            ),

            "description": (
                "First shipments of aid arrive."
            ),

            "source": "Al Jazeera",

            "published":
                "2026-09-12 06:00:00",

            "country": "Pakistan",

            "relevance_score": 6,
        },
    ]

    test_questions = [

        "How has the flooding situation changed over the last two weeks?",

        "Which countries are being affected the most?",

        "How relevant are these articles to my query?",

        "Tell me about the weather",
    ]

    for test_question in test_questions:

        print(
            "\n"
            + "=" * 60
        )

        print(
            f"QUESTION: {test_question}"
        )

        print(
            "=" * 60
        )

        output = generate_visualizations(
            test_articles,
            test_question
        )

        print(
            json.dumps(
                {
                    key: value
                    for key, value
                    in output.items()
                    if key != "data_profile"
                },
                indent=2,
                default=str
            )
        )
