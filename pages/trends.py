import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/trends", name="Daily Trends")

df = pd.read_csv("data/Time.csv")
df["date"] = pd.to_datetime(df["date"])

layout = html.Div([
    html.H3("Daily COVID Cases in South Korea"),
    dcc.Dropdown(
        id="trend-type",
        options=[
            {"label": "Confirmed", "value": "confirmed"},
            {"label": "Deceased", "value": "deceased"},
            {"label": "Recovered", "value": "released"}
        ],
        value="confirmed"
    ),
    dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max()
    ),
    dcc.Graph(id="trend-graph")
])

@dash.callback(
    Output("trend-graph", "figure"),
    Input("trend-type", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_trend_graph(metric, start_date, end_date):
    dff = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    fig = px.line(dff, x="date", y=metric, title=f"{metric.capitalize()} Over Time")
    return fig
