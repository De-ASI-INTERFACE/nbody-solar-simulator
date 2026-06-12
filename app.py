"""N-Body Solar System Simulator — Dash UI Entry Point"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timezone

from simulator.ephemeris import fetch_ephemeris
from simulator.nbody import integrate_nbody
from simulator.bodies import SOLAR_BODIES, BODY_COLORS, BODY_SIZES

app = dash.Dash(
    __name__,
    title="N-Body Solar System Simulator",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = html.Div([
    html.H1("🌌 N-Body Solar System Simulator", style={"textAlign": "center", "color": "#e0e0e0"}),

    html.Div([
        html.Div([
            html.Label("Simulation Duration (days)", style={"color": "#ccc"}),
            dcc.Slider(id="duration-slider", min=30, max=3650, step=30, value=365,
                       marks={30: "1M", 365: "1Y", 1825: "5Y", 3650: "10Y"}),
        ], style={"width": "45%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Bodies", style={"color": "#ccc"}),
            dcc.Checklist(
                id="body-checklist",
                options=[{"label": b, "value": b} for b in SOLAR_BODIES.keys()],
                value=list(SOLAR_BODIES.keys()),
                inline=True,
                style={"color": "#ccc"}
            ),
        ], style={"width": "50%", "display": "inline-block", "padding": "10px"}),
    ], style={"backgroundColor": "#1a1a2e", "padding": "15px", "borderRadius": "8px"}),

    html.Div([
        html.Button("▶ Run Simulation", id="run-btn", n_clicks=0,
                    style={"backgroundColor": "#0f3460", "color": "white",
                           "border": "none", "padding": "10px 25px",
                           "borderRadius": "5px", "cursor": "pointer", "fontSize": "16px"}),
        html.Span(id="status-text", style={"color": "#88c0d0", "marginLeft": "20px"}),
    ], style={"textAlign": "center", "padding": "15px"}),

    dcc.Graph(id="orbit-graph", style={"height": "700px"},
              config={"displayModeBar": True, "scrollZoom": True}),

    html.Div(id="ephemeris-table", style={"padding": "20px"}),

    dcc.Store(id="simulation-data"),
], style={"backgroundColor": "#0d0d1a", "minHeight": "100vh", "fontFamily": "Arial, sans-serif"})


@app.callback(
    Output("simulation-data", "data"),
    Output("status-text", "children"),
    Input("run-btn", "n_clicks"),
    State("duration-slider", "value"),
    State("body-checklist", "value"),
    prevent_initial_call=True,
)
def run_simulation(n_clicks, duration_days, selected_bodies):
    if not selected_bodies:
        return {}, "No bodies selected."

    epoch = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        ephem_data = fetch_ephemeris(selected_bodies, epoch)
        status = f"✅ Ephemeris fetched from NASA JPL Horizons — {epoch}"
    except Exception as e:
        return {}, f"❌ Ephemeris fetch failed: {str(e)}"

    try:
        trajectories = integrate_nbody(ephem_data, duration_days)
        status += f" | Integration: RK45 × {duration_days}d"
    except Exception as e:
        return {}, f"❌ Integration failed: {str(e)}"

    return {"trajectories": trajectories, "bodies": selected_bodies, "epoch": epoch}, status


@app.callback(
    Output("orbit-graph", "figure"),
    Input("simulation-data", "data"),
)
def update_figure(sim_data):
    if not sim_data or "trajectories" not in sim_data:
        fig = go.Figure()
        fig.update_layout(
            scene=dict(bgcolor="#000010"),
            paper_bgcolor="#0d0d1a",
            plot_bgcolor="#0d0d1a",
            title={"text": "Run simulation to view orbits", "font": {"color": "#88c0d0"}},
        )
        return fig

    trajectories = sim_data["trajectories"]
    bodies = sim_data["bodies"]

    traces = []
    for body in bodies:
        if body not in trajectories:
            continue
        traj = trajectories[body]
        x = [p[0] for p in traj]
        y = [p[1] for p in traj]
        z = [p[2] for p in traj]
        color = BODY_COLORS.get(body, "#ffffff")
        size = BODY_SIZES.get(body, 4)

        traces.append(go.Scatter3d(
            x=x, y=y, z=z,
            mode="lines",
            name=body,
            line=dict(color=color, width=2),
        ))
        traces.append(go.Scatter3d(
            x=[x[-1]], y=[y[-1]], z=[z[-1]],
            mode="markers+text",
            name=f"{body} (current)",
            marker=dict(size=size, color=color),
            text=[body],
            textposition="top center",
            textfont=dict(color=color),
            showlegend=False,
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            bgcolor="#000010",
            xaxis=dict(title="X (AU)", gridcolor="#222", color="#666"),
            yaxis=dict(title="Y (AU)", gridcolor="#222", color="#666"),
            zaxis=dict(title="Z (AU)", gridcolor="#222", color="#666"),
        ),
        paper_bgcolor="#0d0d1a",
        font=dict(color="#e0e0e0"),
        legend=dict(bgcolor="#1a1a2e", bordercolor="#333"),
        title=dict(text=f"Solar System Orbits — Epoch {sim_data.get('epoch', '')}",
                   font=dict(color="#88c0d0", size=18)),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    return fig


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
