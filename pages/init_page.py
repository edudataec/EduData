import base64
import dash
import json
import datetime
from dash import Dash, dcc, Output, Input, html, page_container, callback, ctx, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/', name='home')

tab_content1 = dbc.Container([
    dbc.ListGroup(
        [
            
        ],
        id="reciente-list-cont",
        className="mt-3 mb-3",
        style={"height":"60vh"}
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Upload(dbc.Button("BUSCAR", color="primary", className="me-1", id="buscar"), id="buscar_upload"),
                ],
                align="center",
                width="auto"
            ),
            dbc.Col(
                dbc.Button("CREAR NUEVO", color="primary", className="me-1", id="nuevo"),
                align="center",
                width="auto"
            )
        ],
        justify="end",
        className="mb-3"
    )
])
tab_content2 = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div(
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Análisis general de curso", justify="center", className="card-title")),
                                        dbc.CardImg(src="/assets/imgs/plantilla_img1.PNG", top=False)
                                    ],
                                    class_name="flip-card-front", color="primary", inverse=True
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Análisis general de curso", justify="center", className="card-title")),
                                        dbc.CardBody(
                                            [
                                                html.P("Este dashboard es útil para realizar seguimiento de las calificaciones de todo un curso.", className="card-text"),
                                                html.P("Contiene:", className="card-text"),
                                                html.P("-Gráfico de líneas", className="card-text"),
                                                html.P("-Gráfico de dispersión", className="card-text"),
                                                html.P("-Gráfico de barras", className="card-text")
                                            ], 
                                            style={"text-align":"start"}
                                        )
                                    ],
                                    class_name="flip-card-back"
                                ),
                            ],
                            className="flip-card-inner"
                        ),
                        className="mb-3 flip-card",
                        id="card-1"
                    ),
                    html.Div(
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño histórico de materia", justify="center", className="card-title")),
                                        dbc.CardImg(src="/assets/imgs/plantilla_img3.PNG", top=False)
                                    ],
                                    class_name="flip-card-front", color="primary", inverse=True
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño histórico de materia", justify="center", className="card-title")),
                                        dbc.CardBody(
                                            [
                                                html.P("Este dashboard es útil para realizar seguimiento de las calificaciones de una materia a lo largo de varios años.", className="card-text"),
                                                html.P("Contiene:", className="card-text"),
                                                html.P("-Gráfico de líneas", className="card-text"),
                                                html.P("-Gráfico de barras", className="card-text"),
                                                html.P("-Histograma", className="card-text")
                                            ], 
                                            style={"text-align":"start"}
                                        )
                                    ],
                                    class_name="flip-card-back"
                                ),
                            ],
                            className="flip-card-inner"
                        ),
                        className="mb-3 flip-card",
                        id="card-3"
                    ),
                ]
            ),
            dbc.Col(
                [
                   html.Div(
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño individual de estudiantes", justify="center", className="card-title")),
                                        dbc.CardImg(src="/assets/imgs/plantilla_img2.PNG", top=False)
                                    ],
                                    class_name="flip-card-front", color="primary", inverse=True
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño individual de estudiantes", justify="center", className="card-title")),
                                        dbc.CardBody(
                                            [
                                                html.P("Este dashboard es útil para realizar seguimiento de cada estudiante durante el semestre.", className="card-text"),
                                                html.P("Contiene:", className="card-text"),
                                                html.P("-Gráfico de líneas", className="card-text"),
                                                html.P("-Pie chart", className="card-text"),
                                                html.P("-Gráfico de barras", className="card-text")
                                            ], 
                                            style={"text-align":"start"}
                                        )
                                    ],
                                    class_name="flip-card-back"
                                ),
                            ],
                            className="flip-card-inner"
                        ),
                        className="mb-3 flip-card",
                        id="card-2"
                    ),
                    html.Div(
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño de estudiantes por carrera", justify="center", className="card-title")),
                                        dbc.CardImg(src="/assets/imgs/plantilla_img4.PNG", top=False)
                                    ],
                                    class_name="flip-card-front", color="primary", inverse=True
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader(dbc.Row("Desempeño de estudiantes por carrera", justify="center", className="card-title")),
                                        dbc.CardBody(
                                            [
                                                html.P("Este dashboard es útil para realizar seguimiento del desempeño de estudiantes de distintas carreras en una materia", className="card-text"),
                                                html.P("Contiene:", className="card-text"),
                                                html.P("-Gráfico de líneas", className="card-text"),
                                                html.P("-Gráfico de dispersión", className="card-text"),
                                                html.P("-Gráfico de barras", className="card-text"),
                                                html.P("-Gráfico de burbujas", className="card-text")
                                            ], 
                                            style={"text-align":"start"}
                                        )
                                    ],
                                    class_name="flip-card-back"
                                ),
                            ],
                            className="flip-card-inner"
                        ),
                        className="mb-3 flip-card",
                        id="card-4"
                    ),
                ]
            )
        ],
        className="m-3"
    )
)

layout = html.Div(children=[
    dbc.Navbar(
        dbc.Container(
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/imgs/logo.svg", height="40px"))
                    ],
                    align="center",
                    className="g-0"
                )
            )
        ),
        color="primary",
        className="navbar-dark"
    ),
    dbc.Container(children=[
        dbc.Tabs(
            [
                dbc.Tab(label="Recientes", tab_id="recientes"),
                dbc.Tab(label="Plantillas", tab_id="plantillas")
            ],
            id="tabs",
            active_tab="plantillas",
            className="mt-3"
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Nombra tu dashboard")),
                dbc.ModalBody(dbc.Input(id="new_dash_title", placeholder="Escribe el título de tu dashboard", type="text")),
                dbc.ModalFooter(
                    dbc.Button(
                        "CREAR", id="crear_dash"
                    )
                )
            ],
            id="crear_dash_dialg",
            is_open=False
        ),
        html.Div(id="content",),
        html.Div(id="card1t",),
        html.Div(id="card2t",),
        html.Div(id="card3t",),
        html.Div(id="card4t",),
        html.Div(id="button_target")
    ])
])

#Tab callback
@callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "recientes":
        return tab_content1
    elif at == "plantillas":
        return tab_content2

#Lista Recientes callback
@callback(Output("reciente-list-cont", "children"), [Input("tabs", "active_tab")])
def update_recientes_list(x):
    with open("assets/historial_proyectos.json") as json_file:
        proyectos = json.load(json_file)["projects"]

    sorted_proyectos = sorted(proyectos.items(), key=lambda r: r[1]["last_opened"], reverse=True)

    if len(sorted_proyectos)>20:
        sorted_proyectos = sorted_proyectos[0:20]

    list_items = []
    index = 0
    for proyecto in sorted_proyectos:

        dif_datetime = datetime.datetime.now() - datetime.datetime.strptime(proyecto[1]["last_opened"], "%Y-%m-%d %H:%M:%S.%f")

        item = dbc.ListGroupItem(
            dbc.Row(
                [
                    dbc.Col(proyecto[0], width="auto"),
                    dbc.Col("Hace " + str(dif_datetime.days) + " días", width="auto")
                ],
                justify="between"
            ),
            id={"type":"project", "name":proyecto[0], "index":index}
        )
        list_items.append(item)
        index+=1
    return list_items

#Callbacks plantillas
@callback(Output("card1t", "className"), [Input('card-1', 'n_clicks')])
def card_1_click(click):
    print("Card 1")

@callback(Output("card2t", "className"), [Input('card-2', 'n_clicks')])
def card_2_click(click):
    print("Card 2")

@callback(Output("card3t", "className"), [Input('card-3', 'n_clicks')])
def card_3_click(click):
    print("Card 3")

@callback(Output("card4t", "className"), [Input('card-4', 'n_clicks')])
def card_4_click(click):
    print("Card 4")

#Callback botón
@callback(Output("crear_dash_dialg", "is_open"), [Input("nuevo", "n_clicks"), Input("crear_dash", "n_clicks")], State("crear_dash_dialg", "is_open"), prevent_initial_call=True)
def button_func(n1, n3, is_open):
    button_clicked = ctx.triggered_id
    if is_open:
        return not is_open
    else:
        if button_clicked == "nuevo" and n1 is not None:
            return not is_open

#Callback crear dashboard nuevo
@callback(
    Output("project_title", "data"),
    Output("button_target", "children"),
    Output("alertDashboard", "children"),
    Output("statusAlertDashboard", "is_open"),
    Input("crear_dash", "n_clicks"),
    Input({"type":"project", "name":ALL, "index":ALL}, "n_clicks"),
    Input("buscar_upload", "contents"),
    State("new_dash_title", "value"), 
    State("buscar_upload", "filename"),
    prevent_initial_call=True
)
def cargar_dash(n, n2, content, title, filename):
    trigger = ctx.triggered_id
    print(trigger)
    
    if trigger == "crear_dash" and n is not None:
        if new_dash_project(title, None):
            return title + ".json", dcc.Location(pathname="/data", id="id_no_importa"), dash.no_update, dash.no_update
        else:
            return dash.no_update, dash.no_update, "Ya existe un proyecto con el mismo nombre, por favor cambiar el nombre.", True
    elif trigger == "buscar_upload" and content is not None:
        file_end = filename.split(".")[1]
        title = filename.split(".")[0]
        if file_end != "json":
            return dash.no_update, dash.no_update, "No se seleccionó un archivo json.", True
        
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        data = json.loads(decoded)
        if new_dash_project(title, data):
            return title + ".json", dcc.Location(pathname="/data", id="id_no_importa"), dash.no_update, False
        else:
            return dash.no_update, dash.no_update, "Ya existe un proyecto con el mismo nombre, por favor cambiar el nombre.", True
    elif trigger["type"] == "project" and n2[trigger["index"]] is not None:
        update_recent_project(trigger["name"])
        return trigger["name"] + ".json", dcc.Location(pathname="/data", id="id_no_importa"), dash.no_update, dash.no_update
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

def new_dash_project(title, data):
    with open("assets/historial_proyectos.json") as json_file:
        historial = json.load(json_file)

    try:
        history_title = historial["projects"][title]
        return False
    except:
        historial["projects"][title] = {"date_created":datetime.datetime.now().__str__(), "last_opened":datetime.datetime.now().__str__()}

    with open("assets/historial_proyectos.json", "w") as outfile:
        json.dump(historial, outfile)

    if data is not None:
        dash_meta_data = data
    else:
        dash_meta_data = {
            "id":title,
            "data_path":"",
            "contenedores":[],
            "last_selected":"none",
            "selected":"none"
        }
    with open("dashboards/" + title + ".json", "w") as outfile:
        json.dump(dash_meta_data, outfile) 
    
    return True

def update_recent_project(title):
    with open("assets/historial_proyectos.json") as json_file:
        historial = json.load(json_file)

    historial["projects"][title]["last_opened"] = datetime.datetime.now().__str__()

    with open("assets/historial_proyectos.json", "w") as outfile:
        json.dump(historial, outfile)

