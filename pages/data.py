import dash
import os
import re
import json
from dash import Dash, dcc, Output, Input, State, html, page_container, callback, dash_table, ctx
from .utils.util import pandas_load_wrapper
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import tkinter as tk
import plotly.graph_objects as go
from tkinter.filedialog import askopenfilename


dash.register_page(__name__, name='data')

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
                dbc.NavItem(dbc.NavLink("Data", href="/data", active=True))
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
                            html.H3("No hay datos cargados actualmente...", id="no_data_header", style={"text-align":"center"}),
                            html.H2(id="nombre_archivo", className="mt-3", style={"display":"none"}),
                            dbc.Row(
                                dbc.Col(
                                    id="table_cont",
                                    class_name="mt-3",
                                    width="auto"
                                ),
                                id="table_display",
                                justify="end"
                            ),
                            dbc.Row(
                                dbc.Col(
                                    [
                                        html.Div(dbc.Button("CARGAR", color="primary", className="me-1 mt-3 mb-3", id="cargar"), id="cargar_cont"),
                                        html.Div(id="button_func_enabler", style={"display":"none"}),
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
                id="data_page",
                align="center",
                justify="center"
            ),
            fluid=True,
            style={"background-color":"lightgrey", "height":"95vh", "margin":"0"}
        )
    ]
)

@callback(Output("cargar", "disabled"), Output("button_func_enabler", "children"), Input("cargar", "n_clicks"))
def button_disabler(n_clicks):
    if n_clicks is not None:
        return True, "1"
    else:
        return False, None

@callback(Output("data_path", "data"), Output("cargar_cont", "children"), Output("table_display", "style"), Output("nombre_archivo", "style"), Output("no_data_header", "style"), Output("data_page", "style"),
Input("button_func_enabler", "children"), State("data_path", "data"), State("project_title", "data"))
def cargar_data(enable, x, title):
    trigger_id = ctx.triggered_id
    button = dbc.Button("CARGAR", color="primary", className="me-1 mt-3 mb-3", id="cargar")
    file_path = ""
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    if trigger_id == "button_func_enabler" and enable is not None:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file_path = askopenfilename(parent=root)
        root.destroy()
        if file_path!="":
            dash_data["data_path"] = file_path

            with open("dashboards/" + title, "w") as outfile:
                json.dump(dash_data, outfile)
            
            return file_path, button, None, None, {"display":"none"}, {"background-color":"lightgrey", "height":"auto"}
    elif (dash_data["data_path"] != "") :
        file_path = dash_data["data_path"]
        return file_path, button, None, None, {"display":"none"}, {"background-color":"lightgrey", "height":"auto"}
    return dash.no_update, button, dash.no_update, dash.no_update, dash.no_update, dash.no_update

@callback(Output("nombre_archivo", "children"), Input("data_path", "modified_timestamp"), State("data_path", "data"))
def update_title(ts, data):
    print(ts)
    if ts is not None and data is not None:
        print(data)
        return "Archivo cargado: " + os.path.basename(data)

#Callbacks de tabla
@callback(Output("table_cont", "children"), Input("data_path", "modified_timestamp"), State("data_path", "data"))
def load_data(ts, datapath):
    if ts is not None:
        try:
            df = pd.DataFrame()
            df = pandas_load_wrapper(datapath)
        except:
            print("error")

        values=[]
        for column in df.columns:
            li = df[column].tolist()
            values.append(li)

        tabl = go.Figure(
            data=go.Table(
                header=dict(values=list(df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=values,
                            fill_color='lavender',
                            align='left')
            ),
            layout={
                'paper_bgcolor': 'lightgrey',
            }
        )
        return dcc.Graph(figure=tabl,id="table")
    return dash.no_update

@callback(
    Output("dataInfo", "data"),
    Input("data_path", "modified_timestamp"), 
    State("data_path", "data"),
    prevent_initial_call = True
)
def load_data(ts, data_path):
    if ts is not None:
        try:
            df = pd.DataFrame()
            df = pandas_load_wrapper(data_path)
        except:
            print("error")
        return df.to_dict("records")