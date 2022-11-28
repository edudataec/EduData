from threading import Thread
from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import webview

#Dummy recientes
proyectos_recientes = [
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2},
    {"name": "Dashboard1", "dias":2}
]

app = Dash(__name__, external_stylesheets=["assets/css/bootstrap.min.css", "assets/css/style.css"], assets_folder='assets', assets_external_path="",
             assets_url_path="/assets", include_assets_files=True, serve_locally=True)

tab_content1 = dbc.Container([
    dbc.ListGroup(
        [
            
        ],
        id="reciente-list-cont",
        className="mt-3 mb-3"
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("BUSCAR", color="primary", className="me-1"),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("CREAR NUEVO", color="primary", className="me-1"),
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

app.layout = html.Div(children=[
    dbc.Navbar(
        dbc.Container(
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://images.plot.ly/logo/new-branding/plotly-logomark.png", height="40px")),
                        dbc.Col(dbc.NavbarBrand("Titulo", className="ms-2"))
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
        html.Div(id="content",),
        html.Div(id="card1t",),
        html.Div(id="card2t",),
        html.Div(id="card3t",),
        html.Div(id="card4t",)
    ])
])

#Tab callback
@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "recientes":
        return tab_content1
    elif at == "plantillas":
        return tab_content2

#Lista Recientes callback
@app.callback(Output("reciente-list-cont", "children"), [Input("tabs", "active_tab")])
def update_recientes_list(x):
    list_items = []
    for proyecto in proyectos_recientes:
        item = dbc.ListGroupItem(
            dbc.Row(
                [
                    dbc.Col(proyecto["name"], width="auto"),
                    dbc.Col("Hace " + str(proyecto["dias"]) + " días", width="auto")
                ],
                justify="between"
            )
        )
        list_items.append(item)
    return list_items

#Callbacks plantillas
@app.callback(Output("card1t", "className"), [Input('card-1', 'n_clicks')])
def card_1_click(click):
    print("Card 1")

@app.callback(Output("card2t", "className"), [Input('card-2', 'n_clicks')])
def card_2_click(click):
    print("Card 2")

@app.callback(Output("card3t", "className"), [Input('card-3', 'n_clicks')])
def card_3_click(click):
    print("Card 3")

@app.callback(Output("card4t", "className"), [Input('card-4', 'n_clicks')])
def card_4_click(click):
    print("Card 4")

def run_app():
    app.run_server(port=8050, debug=False)

if __name__=='__main__':
    t = Thread(target=run_app)
    t.daemon = True
    t.start()
    window = webview.create_window("PDMAT", "http://127.0.0.1:8050/")
    webview.start(debug=True)