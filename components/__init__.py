"""Competitive Torpedoes - Dashboard section components."""
import streamlit as st


def section_header(icon: str, title: str, subtitle: str):
    """Render a section header with green underline, matching the React design."""
    st.markdown(f"""
    <div style="border-bottom:2px solid rgba(67,217,162,0.3);
                padding-bottom:12px;margin-bottom:24px;margin-top:8px">
        <div style="font-size:20px;font-weight:700;color:#1a1a2e;margin:0;
                    font-family:'DM Sans',sans-serif">
            {icon}&nbsp; {title}
        </div>
        <div style="font-size:13px;color:#888;margin-top:4px;
                    font-family:'DM Sans',sans-serif">
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)
