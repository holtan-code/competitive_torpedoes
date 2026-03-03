"""Competitive Torpedoes - Plotly chart builders."""
import plotly.graph_objects as go
from config import SOCI_GREEN, COMPETITOR_GRAY, BENCHMARK_BLUE

FONT = "DM Sans, -apple-system, sans-serif"
BG = "rgba(0,0,0,0)"
GRID = "#f0f0f4"


def _layout(title="", height=350, **kwargs):
    return dict(
        title=dict(text=title, font=dict(size=15, color="#333", family=FONT), x=0),
        font=dict(family=FONT, color="#555"),
        plot_bgcolor=BG, paper_bgcolor=BG,
        height=height, margin=dict(l=20, r=20, t=50, b=30),
        legend=dict(orientation="h", yanchor="top", y=1.12, xanchor="left", x=0),
        **kwargs,
    )


def horizontal_bar(data: list[dict], title: str) -> go.Figure:
    metrics = [d["metric"] for d in data][::-1]
    soci = [d["soci"] for d in data][::-1]
    comp = [d["compare"] for d in data][::-1]

    fig = go.Figure()
    fig.add_trace(go.Bar(y=metrics, x=comp, name="Competitor", orientation="h",
        marker_color=COMPETITOR_GRAY, marker_cornerradius=6, text=comp, textposition="outside"))
    fig.add_trace(go.Bar(y=metrics, x=soci, name="SOCi", orientation="h",
        marker_color=SOCI_GREEN, marker_cornerradius=6, text=soci, textposition="outside"))
    fig.update_layout(**_layout(title, height=len(data)*70+80),
        barmode="group", xaxis=dict(visible=False), yaxis=dict(automargin=True))
    return fig


def vertical_bar(data: list[dict], title: str, show_benchmark=False,
                 value_format="", height=300) -> go.Figure:
    metrics = [d["metric"] for d in data]
    soci = [d["soci"] for d in data]
    comp = [d["compare"] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=metrics, y=soci, name="SOCi",
        marker_color=SOCI_GREEN, marker_cornerradius=6,
        text=[f"{v}{value_format}" for v in soci], textposition="outside"))
    if show_benchmark and "benchmark" in data[0]:
        bm = [d["benchmark"] for d in data]
        fig.add_trace(go.Bar(x=metrics, y=bm, name="Benchmark",
            marker_color=BENCHMARK_BLUE, marker_cornerradius=6,
            text=[f"{v}{value_format}" for v in bm], textposition="outside"))
    fig.add_trace(go.Bar(x=metrics, y=comp, name="Competitor",
        marker_color=COMPETITOR_GRAY, marker_cornerradius=6,
        text=[f"{v}{value_format}" for v in comp], textposition="outside"))
    fig.update_layout(**_layout(title, height=height),
        barmode="group", yaxis=dict(visible=False), xaxis=dict(tickfont=dict(size=12)))
    return fig


def gauge_chart(title: str, soci_val: float, comp_val: float,
                comp_name: str) -> go.Figure:
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]])
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=soci_val, title={"text": "SOCi"},
        gauge=dict(axis=dict(range=[0, 100]), bar=dict(color=SOCI_GREEN),
                   bgcolor=GRID, shape="angular")), row=1, col=1)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=comp_val, title={"text": comp_name},
        gauge=dict(axis=dict(range=[0, 100]), bar=dict(color=COMPETITOR_GRAY),
                   bgcolor=GRID, shape="angular")), row=1, col=2)
    fig.update_layout(**_layout(title, height=280))
    return fig


def donut_chart(title: str, soci_val: float, comp_val: float,
                comp_name: str) -> go.Figure:
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]])
    for col, (val, name, color) in enumerate([
        (soci_val, "SOCi", SOCI_GREEN),
        (comp_val, comp_name, COMPETITOR_GRAY),
    ], 1):
        fig.add_trace(go.Pie(
            values=[val, 100-val], labels=[name, ""],
            hole=0.65, marker=dict(colors=[color, GRID]),
            textinfo="none", showlegend=False,
            hovertemplate=f"{name}: {val}%<extra></extra>",
        ), row=1, col=col)
        fig.add_annotation(text=f"<b>{val}%</b>", x=0.21 if col==1 else 0.79,
            y=0.5, font=dict(size=22, family=FONT, color="#1a1a2e"),
            showarrow=False)
        fig.add_annotation(text=name, x=0.21 if col==1 else 0.79,
            y=0.3, font=dict(size=12, family=FONT, color="#888"),
            showarrow=False)
    fig.update_layout(**_layout(title, height=260))
    return fig
