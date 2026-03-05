"""Competitive Torpedoes - Social metrics section."""
import streamlit as st
from charts import vertical_bar, donut_chart
from components import section_header

_CHART_CFG = {"displayModeBar": False}


def render(soci: dict, comp: dict, comp_name: str):
    section_header(
        "\U0001F4AC",
        "Social Metrics",
        "Facebook presence, followers, and engagement",
    )

    col1, col2 = st.columns(2)
    with col1:
        fig = vertical_bar(
            [{"metric": "FB Followers", "soci": soci["fbf"], "compare": comp["fbf"]}],
            "Avg. Facebook Follower Count", height=400, comp_name=comp_name,
        )
        st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)
    with col2:
        fig = vertical_bar(
            [{"metric": "Eng/Post", "soci": soci["fbe"], "compare": comp["fbe"]}],
            "Avg. Engagements per Post", height=400, comp_name=comp_name,
        )
        st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)

    col3, col4 = st.columns(2)
    with col3:
        delta = round(soci["er"] - comp["er"], 1)
        color = "#22c55e" if delta > 0 else "#ef4444"
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px 24px;
                    border:1px solid #e8e8ef;box-shadow:0 1px 4px rgba(0,0,0,0.04);
                    height:260px;box-sizing:border-box">
            <h4 style="font-size:15px;font-weight:600;margin:0 0 4px;
                       font-family:'DM Sans',sans-serif">Engagement Rate</h4>
            <p style="font-size:12px;color:#aaa;margin:0 0 18px">
                Avg. engagement rate per post
            </p>
            <div style="display:flex;align-items:flex-end;gap:28px">
                <div>
                    <div style="font-size:11px;color:#43D9A2;font-weight:700;
                                text-transform:uppercase">SOCi</div>
                    <div style="font-size:40px;font-weight:800;color:#1a1a2e;line-height:1">
                        {soci['er']}<span style="font-size:17px;color:#888">%</span>
                    </div>
                </div>
                <div>
                    <div style="font-size:11px;color:#999;font-weight:700;
                                text-transform:uppercase">{comp_name}</div>
                    <div style="font-size:40px;font-weight:800;color:#999;line-height:1">
                        {comp['er']}<span style="font-size:17px;color:#bbb">%</span>
                    </div>
                </div>
                <div style="margin-left:auto;background:{color}12;
                            border-radius:10px;padding:10px 16px">
                    <span style="color:{color};font-weight:700">
                        {abs(delta)}% {'ahead' if delta > 0 else 'behind'}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        fig = donut_chart(
            "% Brands Using Waterfall Posting",
            soci["wp"], comp["wp"], comp_name,
        )
        st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)

