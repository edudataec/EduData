import dash
import os
from dash import Dash, dcc, Output, Input, State, html, page_container, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name='data')

layout = html.Div(
    [
        dbc.NavbarSimple(
            [
                dbc.Container(
                    dcc.Link(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="https://images.plot.ly/logo/new-branding/plotly-logomark.png", height="40px")),
                                dbc.Col(dbc.NavbarBrand("Titulo", className="ms-2"))
                            ],
                            align="center",
                            className="g-0"
                        ),
                        href="/",
                        style={"text-decoration":"none"}
                    ) 
                ),
                dbc.NavItem(dbc.NavLink("Editor", href="/editor")),
                dbc.NavItem(dbc.NavLink("Data", href="/data", active=True)),
                dbc.NavItem(dbc.NavLink("Visualizar", href="/visualizar"))
            ],
            color="primary",
            dark=True,
            links_left=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(id="nombre_archivo"),
                        dbc.Row(
                            dbc.Col(
                                [
                                    dbc.Button("CARGAR", color="primary", className="me-1 mt-3", id="cargar"),
                                    html.Div(id="cargar_target")
                                ],
                                width="auto"
                            ),
                            justify="end"
                        ),
                    ],
                    align="center",
                    width="auto"
                )
            ],
            align="center",
            justify="center",
            style={"background-color":"lightgrey", "height":"95vh"}
        )
    ]
)

@callback(Output("nombre_archivo", "children"), Input("data_path", "modified_timestamp"), State("data_path", "data"))
def update_title(ts, data):
    print("update_title")
    print(ts)
    if ts is not None:
        print(data)
        return os.path.basename(data)