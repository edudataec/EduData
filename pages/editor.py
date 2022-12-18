import json
import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback, State, MATCH, ctx, ALL
from .utils.util import pandas_load_wrapper
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
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(),
                dbc.ModalBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                [],
                                width=4, lg=3, xl=2, xxl=2,
                                id="graph_class_toggle_col"
                            ),
                            dbc.Col(
                                [],
                                width=True,
                                id="graph_class_col"
                            )
                        ],
                        style={"width":"100%", "height":"100%", "margin":"0"}
                    ),
                    style={"padding":"0"}
                ),
            ],
            id="graph_dialg",
            size="xl",
            is_open=False
        ),
    ]
)

#Graph callbacks


#Editor callbacks
@callback(
    Output("graph_dialg", "is_open"),
    Output("graph_class_toggle_col", "children"),
    Output("graph_class_col", "children"),
    Input({"type":"graph", "index":ALL}, "n_clicks"),
    Input({"type":"graph_tog", "name":ALL, "index":ALL}, "n_clicks"),
    Input({"type":"new_graph", "name":ALL, "index":ALL}, "n_clicks"),
    State("graph_dialg", "is_open") 
)
def graph_modal(n, n2, n3, is_open):
    trigger = ctx.triggered_id

    graph_class_toggle_col = [
        html.Div(
            'Simple',
            id={"type":"graph_tog", "name":"simple", "index":"0"},
            className="graph_toggle_selected"
        ),
        html.Div(
            'Distribución',
            id={"type":"graph_tog", "name":"distrib", "index":"1"},
            className="graph_toggle"
        ),
        html.Div(
            'Finanzas',
            id={"type":"graph_tog", "name":"finan", "index":"2"},
            className="graph_toggle"
        ),
        html.Div(
            'Avanzado',
            id={"type":"graph_tog", "name":"adv", "index":"3"},
            className="graph_toggle"
        ),
    ]

    graph_class_col = [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/bar_tr.png",
                            id={"type":"new_graph", "name":"bar", "index":"0"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Gráfico de barras vertical"
                        )
                    ],
                    className="graph_opt_selec"
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/bar_h_tr.png",
                            id={"type":"new_graph", "name":"bar_h", "index":"1"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Gráfico de barras horizontal"
                        )
                    ],
                    className="graph_opt_selec"
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/scatter_tr.png",
                            id={"type":"new_graph", "name":"scatter", "index":"2"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Gráfico de dispersión"
                        )
                    ],
                    className="graph_opt_selec"
                ),
            ],
            className="graph_opt_row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/line_tr.png",
                            id={"type":"new_graph", "name":"line", "index":"3"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Gráfico de líneas"
                        )
                    ],
                    className="graph_opt_selec"
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/bubl_tr.png",
                            id={"type":"new_graph", "name":"bubl", "index":"4"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Gráfico de burbujas"
                        )
                    ],
                    className="graph_opt_selec"
                ),
                html.Div(
                    [
                        html.Img(
                            src="assets/imgs/pie_tr.png",
                            id={"type":"new_graph", "name":"pie", "index":"5"},
                            className="graph_selec_img"
                        ),
                        html.Div(
                            "Pie chart"
                        )
                    ],
                    className="graph_opt_selec"
                ),
            ],
            className="graph_opt_row"
        )
    ]

    if not is_open and trigger["type"] == "graph" and n[int(trigger["index"])-1] is not None:
        return True, graph_class_toggle_col, graph_class_col
    elif trigger["type"] == "graph_tog" and n2[int(trigger["index"])] is not None:
        match trigger["name"]:
            case "simple":
                return True, graph_class_toggle_col, graph_class_col
            case "distrib":
                #Cambiar la opción seleccionada
                graph_class_toggle_col[0] = html.Div(
                                                'Simple',
                                                id={"type":"graph_tog", "name":"simple", "index":"0"},
                                                className="graph_toggle"
                                            )
                graph_class_toggle_col[1] = html.Div(
                                                'Distribución',
                                                id={"type":"graph_tog", "name":"distrib", "index":"1"},
                                                className="graph_toggle_selected"
                                            )
                return True, graph_class_toggle_col, graph_class_col
            case "finan":
                #Cambiar la opción seleccionada
                graph_class_toggle_col[0] = html.Div(
                                                'Simple',
                                                id={"type":"graph_tog", "name":"simple", "index":"0"},
                                                className="graph_toggle"
                                            )
                graph_class_toggle_col[2] = html.Div(
                                                'Finanzas',
                                                id={"type":"graph_tog", "name":"finan", "index":"2"},
                                                className="graph_toggle_selected"
                                            )
                return True, graph_class_toggle_col, graph_class_col
            case "adv":
                #Cambiar la opción seleccionada
                graph_class_toggle_col[0] = html.Div(
                                                'Simple',
                                                id={"type":"graph_tog", "name":"simple", "index":"0"},
                                                className="graph_toggle"
                                            )
                graph_class_toggle_col[3] = html.Div(
                                                'Avanzado',
                                                id={"type":"graph_tog", "name":"adv", "index":"3"},
                                                className="graph_toggle_selected"
                                            )
                return True, graph_class_toggle_col, graph_class_col
            case _:
                return dash.no_update, dash.no_update, dash.no_update
    elif trigger["type"] == "new_graph" and n3[int(trigger["index"])] is not None:
        return False, dash.no_update, dash.no_update
    return dash.no_update, dash.no_update, dash.no_update

@callback(
    Output("main_row", "children"), 
    Input("add-cont-button", "n_clicks"),
    Input("update_editor_target", "children"),
    State("project_title", "data"),
    State("main_row", "children")
)
def update_editor(n_add, update, title, children):
    trigger = ctx.triggered_id
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    print(dash_data)
    content = []

    #Añadir contenedor vacío al json
    if trigger == "add-cont-button" and n_add is not None:
        children.append(add_cont_to_json(n_add, title, dash_data))
        return children

    #Cargar elementos del json
    return render_from_json(dash_data)

def add_cont_to_json(n_add, title, dash_data):

    contenedores = dash_data["contenedores"].copy()
    next_index = int(sorted(contenedores, key=lambda r: int(r["index"]), reverse=True)[0]["index"])+1

    dash_data["contenedores"].append(
        {
            "id":"cont_" + str(next_index),
            "index":str(next_index),
            "width":"4",
            "graph":{
                "type":"none"
            }
        }
    )
    with open("dashboards/" + title, "w") as outfile:
        json.dump(dash_data, outfile) 

    col_buttons_no_graph = html.Div(
                            [
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/add_graph.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"graph", "index":str(next_index)},
                                    className="col-button"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/options.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"config", "index":str(next_index)},
                                    className="col-button"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/remove.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"remove", "index":str(next_index)},
                                    className="col-button"
                                )
                            ],
                            id={"type":"cont_opt", "index":str(next_index)},
                            hidden=True,
                            className="col-buttons-cont-lg"
                        )

    column = dbc.Col(
                        html.Div(
                            [
                                col_buttons_no_graph,
                            ],
                            id={"type":"cont", "index":str(next_index)},
                            className="graph-cont"
                        ),
                        id={"type":"col", "index":str(next_index)},
                        width={"size":4, "order":str(next_index)},
                        className="graph-col"
                    )
    return column

def render_from_json(dash_data):
    content = []
    df = pandas_load_wrapper(dash_data["data_path"])
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
                                    html.Img(
                                        src="assets/imgs/add_graph.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"graph", "index":cont["index"]},
                                    className="col-button-sm"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/options.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"config", "index":cont["index"]},
                                    className="col-button-sm"
                                ),
                                html.Div(
                                    html.Img(
                                        src="assets/imgs/remove.png",
                                        className="cont-opt-img"
                                    ),
                                    id={"type":"remove", "index":cont["index"]},
                                    className="col-button-sm"
                                )
                            ],
                            id={"type":"cont_opt", "index":cont["index"]},
                            hidden=disable_opt,
                            className="col-buttons-cont-sm"
                        )

        match cont["graph"]["type"]:
            case "bar":
                graph = dcc.Graph(
                    figure = px.bar(data_frame=df, x=cont["graph"]["x"], y=cont["graph"]["y"], title=cont["graph"]["title"], barmode=cont["graph"]["barmode"],
                             color=cont["graph"]["color"]), id={'type':cont["graph"]['type'], "index":cont['index']},
                    responsive=True,
                    style={"height":"88%", "width":"100%"}
                )
                content.append(
                    dbc.Col(
                        html.Div(
                            [
                                col_buttons_graph,
                                graph
                            ],
                            id={"type":"cont", "index":cont["index"]},
                            className="graph-cont"
                        ),
                        id={"type":"col", "index":cont["index"]},
                        width={"size":4, "order":cont["index"]},
                        className="graph-col",
                        style=selected_style
                    )
                )
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
                        width={"size":4, "order":cont["index"]},
                        className="graph-col",
                        style=selected_style
                    )
                )
            case _:
                print("Error de render: " + cont["id"])
    return content

#Callback para cualquier opción que requiera cargar de nuevo el editor
@callback(
    Output("update_editor_target", "children"),
    Input({"type":"cont", "index":ALL}, "n_clicks"),
    Input({"type":"remove", "index":ALL}, "n_clicks"),
    Input({"type":"new_graph", "name":ALL, "index":ALL}, "n_clicks"),
    State("project_title", "data"),
    State({"type":"cont_opt", "index":ALL}, "hidden"),
    prevent_initial_call=True
)
def update_selected_cont(n, n2, n3, title, is_not_selected):
    trigger_id = ctx.triggered_id
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    if trigger_id["type"]=="cont" and n[int(trigger_id["index"])-1] is not None and is_not_selected[int(trigger_id["index"])-1]:
        #Se actualiza el contenedor seleccionado en el json
        dash_data['selected'] = trigger_id['index']

        with open("dashboards/" + title, "w") as outfile:
            json.dump(dash_data, outfile) 
        return n
    elif n2[int(trigger_id["index"])-1] is not None and trigger_id["type"]=="remove":
        #Se borra el contenedor seleccionado y se reordena los contenedores en el json
        dash_data["contenedores"][:] = [
            item for item in dash_data["contenedores"] if item.get("index") != trigger_id["index"]
        ]

        dash_data["contenedores"] = sorted(dash_data["contenedores"], key=lambda r: int(r["index"]), reverse=False)

        index = 1
        for cont in dash_data["contenedores"]:
            cont["index"] = str(index)
            index+=1

        print(dash_data["contenedores"])
        
        with open("dashboards/" + title, "w") as outfile:
            json.dump(dash_data, outfile) 
        return n2[int(trigger_id["index"])-1]
    elif trigger_id["type"] == "new_graph" and n3[int(trigger_id["index"])] is not None:
        target_cont = next((item for item in dash_data["contenedores"] if item["index"] == dash_data["selected"]))

        df = pandas_load_wrapper(dash_data["data_path"])
        print(df)

        match trigger_id["name"]:
            case "bar":
                target_cont["graph"] = {
                    "type": "bar",
                    "x": df.columns[0],
                    "y": df.columns[0],
                    "title": "",
                    "barmode": "group",
                    "color": df.columns[0]
                }
            case _:
                target_cont["graph"] = {
                    "type":"none"
                }
        with open("dashboards/" + title, "w") as outfile:
            json.dump(dash_data, outfile) 
        return n3[int(trigger_id["index"])]
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

