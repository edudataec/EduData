import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback
import dash_bootstrap_components as dbc
import tkinter as tk
from tkinter import filedialog

dash.register_page(__name__, name='nodata')

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
                dbc.NavItem(dbc.NavLink("Data", href="/nodata", active=True)),
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
                        html.H3("No hay datos cargados actualmente...", style={"text-align":"center"}),
                        dbc.Row(
                            dbc.Col(
                                [
                                    dbc.Button("CARGAR", color="primary", className="me-1 mt-3", id="cargar"),
                                    html.Div(id="cargar_target")
                                ],
                                width="auto"
                            ),
                            justify="center"
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

@callback(Output("cargar_target", "children"), [Input("cargar", "n_clicks")])
def cargar_data(n):
    if(n is not None):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(file_path)
    return