"""Competitive Torpedoes - Streamlit entry point."""
import streamlit as st
from db import get_all_platforms
from components.header import render_header
from components import overall, search, reputation, social

st.set_page_config(
    page_title="Competitive Torpedoes",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

platform_data = get_all_platforms()

selected_competitor = render_header()

soci = platform_data["SOCi"]
comp = platform_data.get(selected_competitor, platform_data["Yext"])

overall.render(soci, comp, selected_competitor)
st.divider()
search.render(soci, comp, selected_competitor)
st.divider()
reputation.render(soci, comp, selected_competitor)
st.divider()
social.render(soci, comp, selected_competitor)

st.divider()
st.caption(
    "**Note:** All metrics represent averages for the Top 50 brands "
    "(by LVI Score) within each platform. "
    "Connect your database via DATABASE_URL to pull live data."
)
