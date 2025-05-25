import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

toggle_button = dbc.Button(
    "☰", color="primary", outline=True, className="me-2", id="toggle-button", n_clicks=0
)

# Sidebar menu
sidebar = html.Div([
    dbc.Nav(
        [
            dbc.NavLink(
                html.Div(page["name"], className="ms-2"),
                href=page["path"],
                active="exact"
            )
            for page in dash.page_registry.values()
        ],
        vertical=True,
        pills=True
    )
], className="bg-light shadow-sm rounded p-3", id="sidebar")

# Full layout
app.layout = html.Div(style={"backgroundColor": "#f8f9fa", "minHeight": "100vh"}, children=[
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    toggle_button,
                    html.H2("🏥 COVID-19 Dashboard", className="d-inline-block ms-2 mb-0 text-primary fw-bold")
                ], className="d-flex align-items-center")
            ], width=12)
        ], className="bg-white px-4 py-3 shadow-sm rounded mb-3"),

        dbc.Row([
            dbc.Col(sidebar, width=2, id="sidebar-col"),
            dbc.Col(dash.page_container, width=10, id="content-col")
        ], className="g-3")
    ], fluid=True)
])

# Toggle sidebar width on button click
@app.callback(
    Output("sidebar-col", "width"),
    Output("content-col", "width"),
    Output("sidebar-col", "style"),
    Input("toggle-button", "n_clicks"),
    State("sidebar-col", "width"),
)
def toggle_sidebar(n_clicks, sidebar_width):
    if n_clicks:
        if sidebar_width == 2:
            return 0, 12, {"display": "none"}
        else:
            return 2, 10, {}
    return sidebar_width, 10, {}

if __name__ == '__main__':
    port = 8050
    app.run_server(debug=False, host="0.0.0.0", port=port)

