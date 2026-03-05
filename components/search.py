"""Competitive Torpedoes - Search metrics section."""
import streamlit as st
from charts import vertical_bar
from components import section_header
from config import SOCI_GREEN, COMPETITOR_GRAY

_CHART_CFG = {"displayModeBar": False}


def render(soci: dict, comp: dict, comp_name: str):
    section_header(
        "\U0001F50D",
        "Search Metrics",
        "Listing presence, profile completeness, and search visibility",
    )

    st.markdown("**Profile Presence & Completeness**")
    rows = [
        ("Google \u2014 % Claimed & Linked", soci["gc"],  comp["gc"]),
        ("Google \u2014 Avg % Complete",      soci["gpc"], comp["gpc"]),
        ("Yelp \u2014 % Claimed",             soci["yf"],  comp["yf"]),
        ("Yelp \u2014 Avg % Complete",         soci["ypc"], comp["ypc"]),
        ("Facebook \u2014 % Found",            soci["ff"],  comp["ff"]),
        ("Facebook \u2014 Avg % Complete",      soci["fpc"], comp["fpc"]),
    ]
    for label, sv, cv in rows:
        st.markdown(f"""
        <div style="margin:12px 0 4px">
            <div style="font-size:13px;font-weight:600;color:#555;margin-bottom:6px">{label}</div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
                <div style="flex:1;background:#f0f0f4;border-radius:99px;height:8px">
                    <div style="width:{min(sv,100)}%;height:100%;background:{SOCI_GREEN};border-radius:99px"></div>
                </div>
                <div style="min-width:80px;font-size:13px;font-weight:700;color:#333">{sv}% SOCi</div>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
                <div style="flex:1;background:#f0f0f4;border-radius:99px;height:8px">
                    <div style="width:{min(cv,100)}%;height:100%;background:{COMPETITOR_GRAY};border-radius:99px"></div>
                </div>
                <div style="min-width:80px;font-size:13px;color:#666">{cv}% {comp_name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    data = [
        {"metric": "Google 3-Pack",    "soci": soci["g3"], "compare": comp["g3"]},
        {"metric": "Google Local Pg 1", "soci": soci["gl"], "compare": comp["gl"]},
        {"metric": "Yelp Page 1",       "soci": soci["yp"], "compare": comp["yp"]},
    ]
    fig = vertical_bar(data, "Search Rankings", value_format="%", height=520, top_margin=50, comp_name=comp_name)
    st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)
