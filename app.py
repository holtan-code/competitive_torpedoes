"""Competitive Torpedoes - Streamlit entry point."""
import streamlit as st
from db import get_all_platforms
from components.header import render_header
from components import overall, search, reputation, social

st.set_page_config(
    page_title="Local Visibility Index",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

platform_data = get_all_platforms()

selected_competitor = render_header(platform_data)

soci = platform_data["SOCi"]
comp = platform_data.get(selected_competitor, platform_data["Yext"])

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

st.divider()
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
