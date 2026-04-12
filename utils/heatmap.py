import plotly.express as px


def plot_heatmap(data):
    fig = px.density_contour(
        data,
        x="x",
        y="y",
        z="density",
        histfunc="sum",
        title="Live Crowd Density Map",
        labels={"x": "Venue X", "y": "Venue Y", "density": "Crowd Density"},
    )

    fig.update_traces(
        contours_coloring="fill",
        colorscale=["#00E676", "#FFD54F", "#FF1744"],
        showscale=True,
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Outfit, sans-serif"),
        title=dict(font=dict(size=24, color="#ffffff")),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", zeroline=False),
        margin=dict(l=0, r=0, t=60, b=0),
    )

    return fig