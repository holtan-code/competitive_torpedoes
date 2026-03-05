"""Competitive Torpedoes - Header and platform selector."""
import streamlit as st
from config import PLATFORMS


def render_header(platform_data: dict) -> str:
    # ── Top header bar ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#fff;border-bottom:1px solid #e0e0e8;
                box-shadow:0 1px 4px rgba(0,0,0,0.05);
                padding:20px 32px 16px;margin:-1rem -4rem 0;
                font-family:'DM Sans',sans-serif;">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:4px;">
            <div style="width:40px;height:40px;border-radius:10px;
                        background:linear-gradient(135deg,#43D9A2,#2eb88a);
                        display:flex;align-items:center;justify-content:center;
                        font-size:14px;font-weight:800;color:#fff;
                        letter-spacing:-0.5px;flex-shrink:0;">LVI</div>
            <h1 style="font-size:28px;font-weight:700;margin:0;
                       letter-spacing:-0.5px;color:#1a1a2e;">
                Local Visibility Index: Competitive Torpedoes
            </h1>
        </div>
        <p style="color:#888;font-size:14px;margin:0 0 0 54px;">
            2026 Brand Performance Dashboard &mdash; Top 50 by LVI Score
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)

    # ── Controls card ─────────────────────────────────────────────────────────
    with st.container(border=True):
        col_label, col_drop = st.columns([2, 6])

        with col_label:
            st.markdown("""
            <div style="display:flex;align-items:center;gap:8px;min-height:40px;padding:4px 0;">
                <div style="width:14px;height:14px;border-radius:3px;
                            background:#43D9A2;flex-shrink:0;"></div>
                <span style="font-size:14px;font-weight:600;color:#1a1a2e;
                             white-space:nowrap;">SOCi</span>
                <span style="color:#ccc;font-size:16px;margin-left:6px;
                             white-space:nowrap;">vs</span>
            </div>
            """, unsafe_allow_html=True)

        with col_drop:
            dot_col, select_col = st.columns([0.06, 0.94])
            with dot_col:
                st.markdown("""
                <div style="width:14px;height:14px;border-radius:3px;
                            background:#C0C0C0;margin-top:12px;"></div>
                """, unsafe_allow_html=True)
            with select_col:
                selected = st.selectbox(
                    "competitor",
                    PLATFORMS,
                    label_visibility="collapsed",
                    key="competitor_selector",
                )

    return selected
