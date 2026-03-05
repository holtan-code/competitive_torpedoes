"""Competitive Torpedoes - Reputation metrics section."""
import streamlit as st
from charts import vertical_bar, gauge_chart
from components import section_header

_CHART_CFG = {"displayModeBar": False}


def _rating_card(platform: str, soci_val: float, comp_val: float, comp_name: str):
    delta = round(soci_val - comp_val, 1)
    color = "#22c55e" if delta > 0 else "#ef4444"
    st.markdown(f"""
    <div style="background:#fff;border-radius:12px;padding:20px;
                border:1px solid #e8e8ef;text-align:center;
                box-shadow:0 1px 4px rgba(0,0,0,0.04)">
        <h4 style="font-weight:800;margin:0 0 12px;font-size:16px;
                   font-family:'DM Sans',sans-serif">{platform} Rating</h4>
        <div style="display:flex;justify-content:center;gap:20px">
            <div>
                <div style="font-size:28px;font-weight:800;color:#43D9A2">{soci_val}</div>
                <div style="font-size:11px;color:#888">SOCi</div>
            </div>
            <div>
                <div style="font-size:28px;font-weight:800;color:#C0C0C0">{comp_val}</div>
                <div style="font-size:11px;color:#888">{comp_name}</div>
            </div>
        </div>
        <div style="margin-top:8px;font-size:13px;color:{color};font-weight:600">
            SOCi {'+' if delta > 0 else ''}{delta}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render(soci: dict, comp: dict, comp_name: str):
    section_header(
        "\u2B50",
        "Reputation Metrics",
        "Review volume, ratings, and response rates",
    )

    c1, c2 = st.columns(2)
    with c1:
        _rating_card("Google", soci["gr"], comp["gr"], comp_name)
    with c2:
        _rating_card("Yelp",   soci["yr"], comp["yr"], comp_name)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    rc = [
        {"metric": "Google Reviews", "soci": soci["grc"], "compare": comp["grc"]},
        {"metric": "Yelp Reviews",    "soci": soci["yrc"], "compare": comp["yrc"]},
        {"metric": "Facebook Recs",   "soci": soci["frc"], "compare": comp["frc"]},
    ]
    fig = vertical_bar(rc, "Average Review Counts", height=400, comp_name=comp_name)
    st.plotly_chart(fig, use_container_width=True, config=_CHART_CFG)

    col_a, col_b = st.columns(2)
    with col_a:
        gfig = gauge_chart("Review Response Rate", soci["rrp"], comp["rrp"], comp_name)
        st.plotly_chart(gfig, use_container_width=True, config=_CHART_CFG)
    with col_b:
        delta_days = round(comp["rrd"] - soci["rrd"], 1)
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px 24px;
                    border:1px solid #e8e8ef;box-shadow:0 1px 4px rgba(0,0,0,0.04);
                    height:280px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:flex-start;padding-top:8px">
            <h4 style="font-size:15px;font-weight:600;margin:0 0 4px;
                       font-family:'DM Sans',sans-serif">
                Avg. Review Response Time
            </h4>
            <p style="font-size:12px;color:#aaa;margin:0 0 18px">Lower is better</p>
            <div style="display:flex;align-items:flex-end;gap:28px">
                <div>
                    <div style="font-size:11px;color:#43D9A2;font-weight:700;
                                text-transform:uppercase">SOCi</div>
                    <div style="font-size:40px;font-weight:800;color:#1a1a2e;line-height:1">
                        {soci['rrd']}<span style="font-size:17px;color:#888"> days</span>
                    </div>
                </div>
                <div>
                    <div style="font-size:11px;color:#999;font-weight:700;
                                text-transform:uppercase">{comp_name}</div>
                    <div style="font-size:40px;font-weight:800;color:#999;line-height:1">
                        {comp['rrd']}<span style="font-size:17px;color:#bbb"> days</span>
                    </div>
                </div>
                <div style="margin-left:auto;
                            background:{'#22c55e12' if delta_days > 0 else '#ef444412'};
                            border-radius:10px;padding:10px 16px">
                    <span style="color:{'#22c55e' if delta_days > 0 else '#ef4444'};
                                 font-weight:700">
                        {abs(delta_days)} days {'faster' if delta_days > 0 else 'slower'}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

