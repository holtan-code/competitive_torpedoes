"""Competitive Torpedoes - Header and platform selector."""
import streamlit as st
from config import PLATFORMS


def render_header():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:6px">
        <div style="width:38px;height:38px;border-radius:10px;
            background:linear-gradient(135deg,#43D9A2,#2eb88a);
            display:flex;align-items:center;justify-content:center;
            font-size:18px;font-weight:800;color:#fff">CT</div>
        <h1 style="font-size:28px;font-weight:700;margin:0;
            letter-spacing:-0.5px;color:#1a1a2e">Competitive Torpedoes</h1>
    </div>
    <p style="color:#888;font-size:14px;margin:8px 0 0">
        2026 Brand Performance Dashboard &mdash; Top 50 by LVI Score
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns([1, 3])
    with col1:
        selected = st.selectbox(
            "Compare SOCi against:",
            PLATFORMS,
            index=0,
            label_visibility="collapsed",
        )
    with col2:
        st.markdown(
            "<span style=\"color:#888;font-size:13px\">\u25CF SOCi (green) &nbsp; "
            "\u25CF Competitor (gray) &nbsp; \u25CF Benchmark (blue)</span>",
            unsafe_allow_html=True,
        )

    return selected
