import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, name='editor')

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
                dbc.NavItem(dbc.NavLink("Editor", href="/editor", active=True)),
                dbc.NavItem(dbc.NavLink("Data", href="/data")),
                dbc.NavItem(dbc.NavLink("Visualizar", href="/visualizar"))
            ],
            color="primary",
            dark=True,
            links_left=True
        ),
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                    dbc.Col(width=4, style={"background-color":"white", "min-height":"200px", "margin":"10px"}),
                                ],
                                id="main_row"
                            ),
                            html.Div(
                                dbc.Button("+", style={"font-size":"4vh", "border-radius":"100%", "width":"7vh", "height":"7vh"}),
                                style={"position":"fixed", "right":"10px", "bottom":"10px"}
                            )
                        ],
                        id="editor_col",
                        style={"background-color":"lightgrey", "min-height":"100vh", "height":"auto"},
                        width=True
                    ),
                    dbc.Col(
                        [
                            dcc.Markdown("Prueba"),
                            dcc.Markdown("Prueba"),
                            dcc.Markdown("Prueba"),
                            dcc.Markdown("Prueba"),
                            dcc.Markdown("Prueba"),
                            dcc.Markdown("Prueba"),
                        ],
                        id="editor_col",
                        style={"background-color":"white"},
                        width=2
                    )
                ],
                id="main_container",
            ),
            fluid=True
        )
    ]
)