import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/map", name="Geo Map")

df_case = pd.read_csv("data/Case.csv")
df_region = pd.read_csv("data/Region.csv")

df_case["latitude"] = pd.to_numeric(df_case["latitude"], errors="coerce")
df_case["longitude"] = pd.to_numeric(df_case["longitude"], errors="coerce")
df_case = df_case.dropna(subset=["latitude", "longitude"])

df_case_region = pd.merge(df_case, df_region, on=["province", "city"], how="left")
df_case_region = df_case_region[df_case_region["infection_case"].notna()]
df_case_region = df_case_region[df_case_region["infection_case"] != "etc"]

fig = px.scatter_geo(
    df_case_region,
    lat="latitude_x",
    lon="longitude_x",
    size="confirmed",
    color="province",
    hover_name="infection_case",
    projection="natural earth",
    title="Infection Sources by Region (Static Geo Map)",
    height=600
)

# Use projection_scale to zoom into region without cropping
fig.update_geos(
    projection_scale=5,  # Smaller = zoomed in
    center=dict(lat=36.5, lon=127.5),  # Focus on South Korea
    showcountries=True,
    countrycolor="LightGray",
    showland=True,
    landcolor="whitesmoke"
)

layout = html.Div([
    html.H3("Infection Sources - Geographic Map"),
    dcc.Graph(figure=fig, style={"width": "100%", "height": "600px"})
])
