"""Competitive Torpedoes - Streamlit entry point."""
import streamlit as st
from db import get_platform_data
from config import TOP_N
from components.header import render_header
from components import overall, search, reputation, social, brands

st.set_page_config(
    page_title="Local Visibility Index",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected_competitor, mode = render_header()

if mode == "All":
    soci = get_platform_data("SOCi", None)
    comp = get_platform_data(selected_competitor, None)
elif mode == "Match":
    comp = get_platform_data(selected_competitor, None)
    match_n = comp.get("count") or TOP_N
    soci = get_platform_data("SOCi", match_n)
else:  # Top 50
    soci = get_platform_data("SOCi", TOP_N)
    comp = get_platform_data(selected_competitor, TOP_N)

if not comp:
    comp = get_platform_data("Yext", TOP_N)

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

overall.render(soci, comp, selected_competitor)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
st.divider()

search.render(soci, comp, selected_competitor)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
st.divider()

reputation.render(soci, comp, selected_competitor)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
st.divider()

social.render(soci, comp, selected_competitor)
st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
st.divider()

brands.render(selected_competitor, top_n=TOP_N if mode == "Top 50" else None)

st.divider()
if mode == "All":
    st.caption(
        f"**Note:** All metrics represent averages across **all qualifying brands** on each platform — "
        f"**{soci.get('topN', '?')}** SOCi brands vs **{comp.get('topN', '?')}** {selected_competitor} brands."
    )
elif mode == "Match":
    st.caption(
        f"**Note:** Match mode — the top **{soci.get('topN', '?')}** SOCi brands (by LVI Score) are "
        f"compared against all **{comp.get('topN', '?')}** {selected_competitor} brands."
    )
else:
    st.caption(
        "**Note:** All metrics represent averages for the Top 50 brands "
        "(by LVI Score) within each platform."
    )

    if selected_competitor in ("Uberall", "RioSEO"):
        top_n = comp.get("topN", "fewer than 50")
        st.caption(
            f"**Disclaimer:** {selected_competitor} has a limited number of qualifying brands in the LVI dataset. "
            f"Metrics shown reflect averages across only **{top_n} brand{'s' if isinstance(top_n, int) and top_n != 1 else ''}** "
            f"rather than the standard Top 50. Results should be interpreted with this sample size in mind."
        )
