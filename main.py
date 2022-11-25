from threading import Thread
from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import webview

app = Dash(__name__, external_stylesheets=["assets/css/bootstrap.min.css"], assets_folder='assets', assets_external_path="",
             assets_url_path="/assets", include_assets_files=True, serve_locally=True)

tab_content1 = dbc.Container("tab1")
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

def run_app():
    app.run_server(port=8050, debug=False)

if __name__=='__main__':
    t = Thread(target=run_app)
    t.daemon = True
    t.start()
    window = webview.create_window("PDMAT", "http://127.0.0.1:8050/")
    webview.start(debug=True)