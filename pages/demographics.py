import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/demographics", name="Demographics")

df_age = pd.read_csv("data/TimeAge.csv")
df_age["date"] = pd.to_datetime(df_age["date"])

df_gender = pd.read_csv("data/TimeGender.csv")
df_gender["date"] = pd.to_datetime(df_gender["date"])
fig_gender = px.line(df_gender, x="date", y="confirmed", color="sex",
                     title="Confirmed Cases Over Time by Gender")

layout = html.Div([
    html.H3("COVID-19 Trends by Gender and Age"),
    dcc.Graph(figure=fig_gender),
    html.Hr(),
    html.Label("Select Age Group"),
    dcc.Dropdown(
        id="age-dropdown",
        options=[{"label": age, "value": age} for age in df_age["age"].unique()],
        value=df_age["age"].unique()[0]
    ),
    dcc.Graph(id="age-graph")
])

@dash.callback(
    Output("age-graph", "figure"),
    Input("age-dropdown", "value")
)
def update_age_graph(selected_age):
    filtered_df = df_age[df_age["age"] == selected_age]
    fig = px.line(filtered_df, x="date", y="confirmed", title=f"Confirmed Cases for Age Group {selected_age}")
    return fig
