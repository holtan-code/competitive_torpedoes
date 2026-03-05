"""Competitive Torpedoes - Overall scores section."""
import streamlit as st
from charts import horizontal_bar
from components import section_header

_CHART_CFG = {"displayModeBar": False}


def render(soci: dict, comp: dict, comp_name: str):
    section_header(
        "\U0001F4CA",
        "Overall Scores",
        "LVI, Search, Reputation, Social, and AI composite scores",
    )

    data = [
        {"metric": "LVI Score",       "soci": soci["lvi"],    "compare": comp["lvi"]},
        {"metric": "Search Score",     "soci": soci["search"], "compare": comp["search"]},
        {"metric": "Reputation Score", "soci": soci["rep"],    "compare": comp["rep"]},
        {"metric": "Social Score",     "soci": soci["social"], "compare": comp["social"]},
        {"metric": "AI Score",         "soci": soci["ai"],     "compare": comp["ai"]},
    ]

    fig = horizontal_bar(data, f"SOCi vs {comp_name} \u2014 Score Comparison", comp_name=comp_name)
    st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)

