import dash
from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", name="Home")

# Load and prepare data
df_time = pd.read_csv("data/Time.csv")
df_time["date"] = pd.to_datetime(df_time["date"])

total_confirmed = int(df_time["confirmed"].max())
total_released = int(df_time["released"].max())
total_deceased = int(df_time["deceased"].max())
date_min = df_time["date"].min().strftime("%Y-%m-%d")
date_max = df_time["date"].max().strftime("%Y-%m-%d")

layout = html.Div([
    html.H2("Welcome to the COVID-19 Dashboard"),
    html.P(f"This dashboard presents interactive insights into the COVID-19 outbreak in South Korea."),
    html.P(f"Data covers the period from {date_min} to {date_max}."),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Confirmed", className="card-title"),
                html.H3(f"{total_confirmed:,}")
            ])
        ], color="primary", inverse=True)),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Recovered", className="card-title"),
                html.H3(f"{total_released:,}")
            ])
        ], color="success", inverse=True)),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Deceased", className="card-title"),
                html.H3(f"{total_deceased:,}")
            ])
        ], color="danger", inverse=True)),
    ], className="mb-4"),
    
    html.H4("Explore the Dashboard"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Daily Trends"),
                html.P("Visualize confirmed, deceased, and recovered cases over time."),
                dcc.Link("Go to Trends →", href="/trends")
            ])
        ])),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Demographics"),
                html.P("Explore COVID-19 impact by gender and age group."),
                dcc.Link("Go to Demographics →", href="/demographics")
            ])
        ])),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Infection Sources"),
                html.P("View the top infection sources and their case counts."),
                dcc.Link("Go to Infection Sources →", href="/infections")
            ])
        ])),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Geo Map"),
                html.P("Visualize geographic distribution of cases."),
                dcc.Link("Go to Geo Map →", href="/map")
            ])
        ]))
    ])
])
