import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/infections", name="Infection Sources")

df_case = pd.read_csv("data/Case.csv")
df_region = pd.read_csv("data/Region.csv")

df_case["latitude"] = pd.to_numeric(df_case["latitude"], errors="coerce")
df_case["longitude"] = pd.to_numeric(df_case["longitude"], errors="coerce")
df_case = df_case.dropna(subset=["latitude", "longitude"])

df_case_region = pd.merge(df_case, df_region, on=["province", "city"], how="left")
df_case_region = df_case_region[df_case_region["infection_case"].notna()]
df_case_region = df_case_region[df_case_region["infection_case"] != "etc"]

top_sources = (
    df_case_region.groupby("infection_case")["confirmed"]
    .sum()
    .reset_index()
    .sort_values("confirmed", ascending=False)
    .head(10)
)

fig = px.bar(
    top_sources,
    x="confirmed",
    y="infection_case",
    orientation="h",
    title="Top 10 Infection Sources by Confirmed Cases",
    labels={"confirmed": "Confirmed Cases", "infection_case": "Infection Source"},
    height=500
)
fig.update_layout(yaxis=dict(categoryorder="total ascending"))

layout = html.Div([
    html.H3("Top Infection Sources"),
    dcc.Graph(figure=fig)
])
