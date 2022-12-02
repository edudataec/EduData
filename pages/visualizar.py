import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name='visualizar')

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
                dbc.NavItem(dbc.NavLink("Data", href="/nodata")),
                dbc.NavItem(dbc.NavLink("Visualizar", href="/visualizar", active=True))
            ],
            color="primary",
            dark=True,
            links_left=True
        ),
        html.Div("VISUALIZAR")
    ]
)