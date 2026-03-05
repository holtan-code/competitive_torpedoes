"""Competitive Torpedoes - Plotly chart builders."""
import plotly.graph_objects as go
from config import SOCI_GREEN, COMPETITOR_GRAY, BENCHMARK_BLUE

FONT = "'DM Sans', -apple-system, sans-serif"
BG   = "#fff"
GRID = "#f0f0f4"


def _layout(title="", height=350, **kwargs):
    d = dict(
        title=dict(text=title, font=dict(size=15, color="#333", family=FONT), x=0),
        font=dict(family=FONT, color="#555"),
        plot_bgcolor=BG, paper_bgcolor=BG,
        height=height,
        margin=dict(l=20, r=20, t=50, b=30),
    )
    d.update(kwargs)  # caller kwargs override defaults
    return d


def horizontal_bar(data: list[dict], title: str, comp_name="Competitor") -> go.Figure:
    """Horizontal grouped bar — SOCi (top) vs Competitor (bottom), legend below."""
    metrics = [d["metric"] for d in data][::-1]
    soci    = [d["soci"]    for d in data][::-1]
    comp    = [d["compare"] for d in data][::-1]

    fig = go.Figure()

    # Competitor added first → renders below SOCi in the group
    fig.add_trace(go.Bar(
        y=metrics, x=comp,
        name=comp_name, orientation="h",
        marker_color=COMPETITOR_GRAY, marker_cornerradius=6,
        text=comp, textposition="outside",
        textfont=dict(color="#666", size=13, family=FONT),
        hovertemplate=f"{comp_name}: %{{x}}<extra></extra>",
    ))

    # SOCi added second → renders on top in the group
    fig.add_trace(go.Bar(
        y=metrics, x=soci,
        name="SOCi", orientation="h",
        marker_color=SOCI_GREEN, marker_cornerradius=6,
        text=soci, textposition="outside",
        textfont=dict(color="#333", size=13, family=FONT),
        hovertemplate="SOCi: %{x}<extra></extra>",
    ))

    fig.update_layout(
        **_layout(title, height=len(data) * 70 + 80, margin=dict(l=20, r=20, t=50, b=50)),
        barmode="group",
        legend=dict(orientation="h", yanchor="top", y=-0.08,
                    xanchor="left", x=0, font=dict(size=12),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(
            automargin=True,
            tickfont=dict(size=13, color="#555", family=FONT),
            showgrid=False,
        ),
    )
    return fig


def vertical_bar(data: list[dict], title: str, show_benchmark=False,
                 value_format="", height=300, top_margin=85, legend_y=1.14,
                 comp_name="Competitor") -> go.Figure:
    metrics = [d["metric"] for d in data]
    soci    = [d["soci"]   for d in data]
    comp    = [d["compare"] for d in data] if data and "compare" in data[0] else []

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=metrics, y=soci, name="SOCi",
        marker_color=SOCI_GREEN, marker_cornerradius=6,
        text=[f"{v}{value_format}" for v in soci], textposition="outside",
        textfont=dict(size=12, family=FONT),
        hovertemplate="SOCi: %{y}<extra></extra>",
    ))
    if show_benchmark and data and "benchmark" in data[0]:
        bm = [d["benchmark"] for d in data]
        fig.add_trace(go.Bar(
            x=metrics, y=bm, name="Benchmark",
            marker_color=BENCHMARK_BLUE, marker_cornerradius=6,
            text=[f"{v}{value_format}" for v in bm], textposition="outside",
            textfont=dict(size=12, family=FONT),
            hovertemplate="Benchmark: %{y}<extra></extra>",
        ))
    if comp:
        fig.add_trace(go.Bar(
            x=metrics, y=comp, name=comp_name,
            marker_color=COMPETITOR_GRAY, marker_cornerradius=6,
            text=[f"{v}{value_format}" for v in comp], textposition="outside",
            textfont=dict(size=12, family=FONT),
            hovertemplate="Competitor: %{y}<extra></extra>",
        ))

    all_vals = soci + comp + ([d["benchmark"] for d in data] if show_benchmark and data and "benchmark" in data[0] else [])
    y_max = max(all_vals) * 1.3 if all_vals else 100

    fig.update_layout(
        **_layout(title, height=height, margin=dict(l=20, r=20, t=top_margin, b=50)),
        barmode="group",
        legend=dict(orientation="h", yanchor="top", y=-0.08,
                    xanchor="left", x=0, font=dict(size=12),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        yaxis=dict(visible=False, showgrid=False, range=[0, y_max]),
        xaxis=dict(tickfont=dict(size=12, family=FONT), showgrid=False),
    )
    return fig


def gauge_chart(title: str, soci_val: float, comp_val: float,
                comp_name: str) -> go.Figure:
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=2,
                        specs=[[{"type": "indicator"}, {"type": "indicator"}]])

    def _gauge(val, color):
        return dict(
            axis=dict(range=[0, 100], visible=False),
            bar=dict(color="rgba(0,0,0,0)", thickness=0),
            bgcolor="rgba(0,0,0,0)",
            shape="angular",
            steps=[
                dict(range=[0, val],       color=color),
                dict(range=[val, 100],     color=GRID),
            ],
        )

    fig.add_trace(go.Indicator(
        mode="gauge+number", value=soci_val,
        title={"text": "SOCi", "font": {"size": 14, "color": "#555", "family": FONT}},
        number={"suffix": "%", "font": {"size": 28, "color": "#333", "family": FONT}},
        gauge=_gauge(soci_val, SOCI_GREEN),
    ), row=1, col=1)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=comp_val,
        title={"text": comp_name, "font": {"size": 14, "color": "#555", "family": FONT}},
        number={"suffix": "%", "font": {"size": 28, "color": "#333", "family": FONT}},
        gauge=_gauge(comp_val, COMPETITOR_GRAY),
    ), row=1, col=2)
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
            values=[val, 100 - val], labels=[name, ""],
            hole=0.65, marker=dict(colors=[color, GRID]),
            textinfo="none", showlegend=False,
            hovertemplate=f"{name}: {val}%<extra></extra>",
        ), row=1, col=col)
        fig.add_annotation(
            text=f"<b>{val}%</b>",
            x=0.21 if col == 1 else 0.79, y=0.55,
            xanchor="center", yanchor="middle",
            font=dict(size=22, family=FONT, color="#1a1a2e"),
            showarrow=False,
        )
        fig.add_annotation(
            text=name,
            x=0.21 if col == 1 else 0.79, y=0.38,
            xanchor="center", yanchor="middle",
            font=dict(size=12, family=FONT, color="#888"),
            showarrow=False,
        )
    fig.update_layout(**_layout(title, height=260))
    return fig
