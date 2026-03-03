"""Competitive Torpedoes - Social metrics section."""
import streamlit as st
from charts import vertical_bar, donut_chart
from ai_analysis import analyze_section


def render(soci: dict, comp: dict, comp_name: str):
    st.subheader("\U0001F4AC Social Metrics")
    st.caption("Facebook presence, followers, and engagement")

    col1, col2 = st.columns(2)
    with col1:
        fig = vertical_bar(
            [{"metric": "FB Followers", "soci": soci["fbf"], "compare": comp["fbf"]}],
            "Avg. Facebook Follower Count", height=260)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = vertical_bar(
            [{"metric": "Eng/Post", "soci": soci["fbe"], "compare": comp["fbe"]}],
            "Avg. Engagements per Post", height=260)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        delta = round(soci["er"] - comp["er"], 1)
        color = "#22c55e" if delta > 0 else "#ef4444"
        st.markdown(f"""
        <div style="background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #e8e8ef">
            <h4 style="font-size:15px;font-weight:600;margin:0 0 4px">Engagement Rate</h4>
            <p style="font-size:12px;color:#aaa;margin:0 0 18px">Avg. engagement rate per post</p>
            <div style="display:flex;align-items:flex-end;gap:28px">
                <div>
                    <div style="font-size:11px;color:#43D9A2;font-weight:700;text-transform:uppercase">SOCi</div>
                    <div style="font-size:40px;font-weight:800;color:#1a1a2e;line-height:1">{soci['er']}<span style="font-size:17px;color:#888">%</span></div>
                </div>
                <div>
                    <div style="font-size:11px;color:#999;font-weight:700;text-transform:uppercase">{comp_name}</div>
                    <div style="font-size:40px;font-weight:800;color:#999;line-height:1">{comp['er']}<span style="font-size:17px;color:#bbb">%</span></div>
                </div>
                <div style="margin-left:auto;background:{color}12;border-radius:10px;padding:10px 16px">
                    <span style="color:{color};font-weight:700">{abs(delta)}% {'ahead' if delta>0 else 'behind'}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        fig = donut_chart("% Brands Using Waterfall Posting",
                          soci["wp"], comp["wp"], comp_name)
        st.plotly_chart(fig, use_container_width=True)

    ctx = {
        "fb_followers": {"soci": soci["fbf"], "comp": comp["fbf"]},
        "fb_engagements": {"soci": soci["fbe"], "comp": comp["fbe"]},
        "engagement_rate": {"soci": soci["er"], "comp": comp["er"]},
        "waterfall_pct": {"soci": soci["wp"], "comp": comp["wp"]},
        "competitor": comp_name,
    }
    key = "ai_social_metrics"
    with st.expander("\u2728 Analyze Social Metrics", expanded=False):
        if st.button("Generate Talking Points", key=f"{key}_btn"):
            with st.spinner("Analyzing..."):
                result = analyze_section("Social Metrics", ctx, comp_name)
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
                    st.markdown(analyze_section("Social Metrics", ctx, comp_name, conversation=conv))
