import json
import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback, State, MATCH, ctx
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

                                ],
                                id="main_row"
                            ),
                            html.Div(
                                dbc.Button("+", id="add-cont-button", style={"font-size":"4vh", "border-radius":"100%", "width":"7vh", "height":"7vh"}),
                                style={"position":"fixed", "right":"10px", "bottom":"10px"}
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        html.Img(
                                            src="assets/imgs/arrows.png",
                                            id="slider-button"
                                        ),
                                        className="slider-button-cont"
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button("IMPORTAR", id="imp_button"),
                                            dbc.Button("EXPORTAR", id="exp_button")
                                        ],
                                        className="slider-opt-cont"
                                    ),
                                ],
                                id="options-slider-cont",
                                className="options-slider-cont-up"
                            ),
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

#Editor callbacks
@callback(
    Output("main_row", "children"), 
    Input("add-cont-button", "n_clicks"), 
    State("main_row", "children"), 
    State("project_title", "data")
)
def update_editor(n_clicks, children, title):
    trigger = ctx.triggered_id
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    print(dash_data)
    content = []

    #Añadir contenedor
    if trigger == "add-cont-button":
        dash_data["contenedores"].append(
            {
                "id":"cont_" + str(n_clicks),
                "index":str(n_clicks),
                "width":"4",
                "graph":{
                    "type":"none"
                }
            }
        )
        with open("dashboards/" + title, "w") as outfile:
            json.dump(dash_data, outfile) 

    #Cargar elementos del json

    for cont in dash_data["contenedores"]:

        if cont["index"] == dash_data["selected"]:
            disable_opt = False
        else:
            disable_opt = True

        col_buttons_graph = html.Div(
                            [
                                html.Div(
                                    id={"type":"graph", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    id={"type":"config", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    id={"type":"remove", "index":cont["index"]},
                                    className="col-button"
                                )
                            ],
                            id={"type":"cont_opt", "index":cont["index"]},
                            hidden=disable_opt,
                            className="col-buttons-cont-lg"
                        )

        col_buttons_no_graph = html.Div(
                            [
                                html.Div(
                                    id={"type":"graph", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    id={"type":"config", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    id={"type":"remove", "index":cont["index"]},
                                    className="col-button"
                                )
                            ],
                            id={"type":"cont_opt", "index":cont["index"]},
                            hidden=disable_opt,
                            className="col-buttons-cont-sm"
                        )

        print(cont["graph"]["type"])
        match cont["graph"]["type"]:
            case "bar":
                graph = dcc.Graph(figure = px.bar(data_frame=df, x=cont["graph"]["x"], y=cont["graph"]["y"], title=cont["graph"]["title"], barmode=cont["graph"]["barmode"], color=cont["graph"]["color"]), id={'type':cont["graph"]['type'], "index":cont['index']})
                content.append(dbc.Col(graph, id=cont["id"], width=cont["width"]))
            case "none":
                content.append(
                    dbc.Col(
                        col_buttons_graph,
                        id={"type":"cont", "index":cont["index"]},
                        width=4,
                        className="graph-cont"
                    )
                )
            case default:
                print("Error de render: " + cont["id"])
    return content


#Options callbacks
@callback(Output("options-slider-cont", "className"), Input("slider-button", "n_clicks"), State("options-slider-cont", "className"))
def slide_down(n_clicks, className):
    if className == "options-slider-cont-up":
        return "options-slider-cont-down"
    elif className == "options-slider-cont-down":
        return "options-slider-cont-up"

