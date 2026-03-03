"""Competitive Torpedoes - Overall scores section."""
import streamlit as st
from charts import horizontal_bar
from ai_analysis import analyze_section


def render(soci: dict, comp: dict, comp_name: str):
    st.subheader("\U0001F4CA Overall Scores")
    st.caption("LVI, Search, Reputation, Social, and AI composite scores")

    data = [
        {"metric": "LVI Score",        "soci": soci["lvi"],    "compare": comp["lvi"]},
        {"metric": "Search Score",      "soci": soci["search"], "compare": comp["search"]},
        {"metric": "Reputation Score",  "soci": soci["rep"],    "compare": comp["rep"]},
        {"metric": "Social Score",      "soci": soci["social"], "compare": comp["social"]},
        {"metric": "AI Score",          "soci": soci["ai"],     "compare": comp["ai"]},
    ]

    fig = horizontal_bar(data, f"SOCi vs {comp_name} \u2014 Score Comparison")
    st.plotly_chart(fig, use_container_width=True)

    ctx = {"scores": data, "soci_brands": soci.get("brand_count", 474),
           "competitor": comp_name, "comp_brands": comp.get("brand_count", 50)}
    _render_analysis("Overall Scores", ctx, comp_name)


def _render_analysis(title, ctx, comp_name):
    key = f"ai_{title.replace(' ', '_').lower()}"
    with st.expander(f"\u2728 Analyze {title}", expanded=False):
        if st.button("Generate Talking Points", key=f"{key}_btn"):
            with st.spinner("Analyzing..."):
                result = analyze_section(title, ctx, comp_name)
                st.session_state[key] = result
        if key in st.session_state:
            st.markdown(st.session_state[key])
            follow_up = st.text_input("Ask a follow-up:", key=f"{key}_fu",
                                       placeholder="e.g. How should I position this in a pitch?")
            if follow_up:
                conv = [
                    {"role": "user", "content": f"Data: {ctx}"},
                    {"role": "assistant", "content": st.session_state[key]},
                    {"role": "user", "content": follow_up},
                ]
                with st.spinner("Thinking..."):
                    reply = analyze_section(title, ctx, comp_name, conversation=conv)
                    st.markdown(reply)
