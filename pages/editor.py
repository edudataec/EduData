import json
import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback, State, MATCH, ctx, ALL
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
                        id="config_col",
                        class_name="config-col-closed",
                        width=2
                    ),
                    html.Div(id="update_editor_target", hidden=True)
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
    Input("update_editor_target", "children"),
    State("project_title", "data")
)
def update_editor(n_add, update, title):
    trigger = ctx.triggered_id
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    print(dash_data)
    content = []

    #Añadir contenedor vacío al json
    if trigger == "add-cont-button":
        add_cont_to_json(n_add, title, dash_data)

    #Cargar elementos del json
    return render_from_json(dash_data)

def add_cont_to_json(n_add, title, dash_data):
    dash_data["contenedores"].append(
        {
            "id":"cont_" + str(n_add),
            "index":str(n_add),
            "width":"4",
            "graph":{
                "type":"none"
            }
        }
    )
    with open("dashboards/" + title, "w") as outfile:
        json.dump(dash_data, outfile) 

def render_from_json(dash_data):
    content = []
    for cont in dash_data["contenedores"]:

        if cont["index"] == dash_data["selected"]:
            disable_opt = False
            selected_style = {"border-color":"lightskyblue"}
        else:
            disable_opt = True
            selected_style = {}

        col_buttons_no_graph = html.Div(
                            [
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/add_graph.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"graph", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/options.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"config", "index":cont["index"]},
                                    className="col-button"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/remove.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"remove", "index":cont["index"]},
                                    className="col-button"
                                )
                            ],
                            id={"type":"cont_opt", "index":cont["index"]},
                            hidden=disable_opt,
                            className="col-buttons-cont-lg"
                        )

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
                            className="col-buttons-cont-sm"
                        )

        match cont["graph"]["type"]:
            case "bar":
                graph = dcc.Graph(figure = px.bar(data_frame=df, x=cont["graph"]["x"], y=cont["graph"]["y"], title=cont["graph"]["title"], barmode=cont["graph"]["barmode"], color=cont["graph"]["color"]), id={'type':cont["graph"]['type'], "index":cont['index']})
                content.append(dbc.Col(graph, id=cont["id"], width=cont["width"]))
            case "none":
                content.append(
                    dbc.Col(
                        html.Div(
                            [
                                col_buttons_no_graph,
                            ],
                            id={"type":"cont", "index":cont["index"]},
                            className="graph-cont"
                        ),
                        id={"type":"col", "index":cont["index"]},
                        width=4,
                        className="graph-col",
                        style=selected_style
                    )
                )
            case default:
                print("Error de render: " + cont["id"])
    return content

#Callback
@callback(
    Output("update_editor_target", "children"),
    Input({"type":"cont", "index":ALL}, "n_clicks"),
    State("project_title", "data"),
    State({"type":"cont_opt", "index":ALL}, "hidden"),
    prevent_initial_call=True
)
def update_selected_cont(n, title, is_not_selected):
    trigger_id = ctx.triggered_id
    if trigger_id["type"]=="cont":
        if n[int(trigger_id["index"])-1] is not None and is_not_selected[int(trigger_id["index"])-1]:
            print(n[int(trigger_id["index"])-1])
            with open("dashboards/" + title) as json_file:
                dash_data = json.load(json_file)

            dash_data['selected'] = trigger_id['index']

            with open("dashboards/" + title, "w") as outfile:
                json.dump(dash_data, outfile) 
            return n
    return dash.no_update

#Callback para abrir opciones
@callback(Output("config_col", "class_name"), Input({"type":"config", "index":ALL}, "n_clicks"), State("config_col", "class_name"), prevent_initial_call=True)
def switch_graph_config(n, classname):
    trigger_id = ctx.triggered_id
    if n[int(trigger_id["index"])-1] is not None:
        if classname == "config-col-closed":
            return "config-col-open"
        if classname == "config-col-open":
            return "config-col-closed"
    return dash.no_update

#Options callbacks
@callback(Output("options-slider-cont", "className"), Input("slider-button", "n_clicks"), State("options-slider-cont", "className"))
def slide_down(n_clicks, className):
    if className == "options-slider-cont-up":
        return "options-slider-cont-down"
    elif className == "options-slider-cont-down":
        return "options-slider-cont-up"

