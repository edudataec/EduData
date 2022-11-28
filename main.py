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
tab_content2 = dbc.Container("tab2")

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
        html.Div(id="content")
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

def run_app():
    app.run_server(port=8050, debug=False)

if __name__=='__main__':
    t = Thread(target=run_app)
    t.daemon = True
    t.start()
    window = webview.create_window("PDMAT", "http://127.0.0.1:8050/")
    webview.start(debug=True)