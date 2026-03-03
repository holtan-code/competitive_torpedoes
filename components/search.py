"""Competitive Torpedoes - Search metrics section."""
import streamlit as st
from charts import vertical_bar
from ai_analysis import analyze_section
from config import SOCI_GREEN, COMPETITOR_GRAY


def render(soci: dict, comp: dict, comp_name: str):
    st.subheader("\U0001F50D Search Metrics")
    st.caption("Listing presence, profile completeness, and search visibility")

    st.markdown("**Profile Presence & Completeness**")
    rows = [
        ("Google \u2014 % Claimed & Linked", soci["gc"], comp["gc"]),
        ("Google \u2014 Avg % Complete",      soci["gpc"], comp["gpc"]),
        ("Yelp \u2014 % Claimed",             soci["yf"],  comp["yf"]),
        ("Yelp \u2014 Avg % Complete",         soci["ypc"], comp["ypc"]),
        ("Facebook \u2014 % Found",            soci["ff"],  comp["ff"]),
        ("Facebook \u2014 Avg % Complete",      soci["fpc"], comp["fpc"]),
    ]
    for label, sv, cv in rows:
        st.markdown(f"<div style=\"font-size:13px;font-weight:600;color:#555;margin:12px 0 4px\">{label}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([5, 1])
        with c1:
            st.progress(sv / 100)
        with c2:
            st.markdown(f"**{sv}%** SOCi")
        c3, c4 = st.columns([5, 1])
        with c3:
            st.progress(cv / 100)
        with c4:
            st.markdown(f"{cv}% {comp_name}")

    st.markdown("---")

    data = [
        {"metric": "Google 3-Pack",     "soci": soci["g3"], "benchmark": 24, "compare": comp["g3"]},
        {"metric": "Google Local Pg 1",  "soci": soci["gl"], "benchmark": 2,  "compare": comp["gl"]},
        {"metric": "Yelp Page 1",        "soci": soci["yp"], "benchmark": 23, "compare": comp["yp"]},
    ]
    fig = vertical_bar(data, "Search Rankings", show_benchmark=True, value_format="%", height=320)
    st.plotly_chart(fig, use_container_width=True)

    ctx = {"profiles": rows, "rankings": data, "competitor": comp_name}
    key = "ai_search_metrics"
    with st.expander("\u2728 Analyze Search Metrics", expanded=False):
        if st.button("Generate Talking Points", key=f"{key}_btn"):
            with st.spinner("Analyzing..."):
                result = analyze_section("Search Metrics", ctx, comp_name)
                st.session_state[key] = result
        if key in st.session_state:
            st.markdown(st.session_state[key])
            fu = st.text_input("Ask a follow-up:", key=f"{key}_fu")
            if fu:
                conv = [
                    {"role": "user", "content": f"Data: {ctx}"},
                    {"role": "assistant", "content": st.session_state[key]},
                    {"role": "user", "content": fu},
                ]
                with st.spinner("Thinking..."):
                    st.markdown(analyze_section("Search Metrics", ctx, comp_name, conversation=conv))
