import platform
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
            [
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
                                            html.Div(id="cargar_target"),
                                            html.Div(id="edit_tg")
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
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Carga tus datos")),
                        dbc.ModalBody(dbc.Input(id="cargar_dash_data", placeholder="Escribe la ubicación del archivo en tu computadora.", type="text")),
                        dbc.ModalFooter(
                            dbc.Button(
                                "CARGAR", id="cargar_data_modal"
                            )
                        )
                    ],
                    id="cargar_data_dialg",
                    is_open=False
                ),
            ],
            fluid=True,
            style={"background-color":"lightgrey", "height":"95vh", "margin":"0"}
        ),
        html.Div(id="force_refresh_data",hidden=True)
    ]
)

@callback(Output("edit_tg", "children"), Input("editor_nav", "n_clicks"))
def edit_nav(n1):
    if n1 is not None:
        return dcc.Location(pathname="/editor", id="id_no_importa2")

@callback(Output("cargar", "disabled"), Output("button_func_enabler", "children"), Input("cargar", "n_clicks"), Input("cargar_data_dialg", "is_open"))
def button_disabler(n_clicks, is_open):
    if ctx.triggered_id=="cargar" and n_clicks is not None:
        return True, "1"
    elif ctx.triggered_id=="cargar_data_dialg":
        if is_open == False:
            return False, dash.no_update
        else:
            return True, dash.no_update
    else:
        return False, None

@callback(
    Output("cargar_dash_data", "value"), Output("cargar_data_dialg","is_open"), Output("cargar_data_modal", "n_clicks"),
    Output("force_refresh_data", "children"), Input("button_func_enabler", "children"),
    State("data_path", "data"), State("project_title", "data")
)
def cargar_data(enable, x, title):
    trigger_id = ctx.triggered_id
    file_path = ""
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    if trigger_id == "button_func_enabler" and enable is not None:
        print(enable)
        sys = 'Darwin'
        if sys != 'Darwin':
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            file_path = askopenfilename(parent=root)
            root.destroy()
            if file_path!="":
                #User selecciona archivo
                return file_path, False, 1, 1
            elif (dash_data["data_path"] != "") :
                print(dash_data["data_path"])
                #User no selecciona archivo pero ya tiene datos cargados
                return dash_data["data_path"], False, 1, 1
            else:
                #User no selecciona archivo pero tampoco tiene datos cargados
                return file_path, False, 1, 1
        else:
            return None, True, None, dash.no_update
    elif (dash_data["data_path"] != "") :
        #User tiene datos cargados y no aplastó el boton de cargar datos
        file_path = dash_data["data_path"]
        return file_path, False, 1, 1
    #User no tiene datos cargados y no aplastó el boton de cargar datos o no seleccionó datos
    return dash.no_update, False, None, dash.no_update

@callback(Output("data_path", "data"), Input("cargar_data_modal", "n_clicks"), State("cargar_dash_data", "value"), prevent_initial_call=True)
def modal_input(n, value):
    if n is not None:
        return value
    else:
        return dash.no_update

#Callbacks de tabla
@callback(
    Output("table_cont", "children"), Output("nombre_archivo", "children"),
    Output("cargar_cont", "children"), Output("table_display", "style"),
    Output("nombre_archivo", "style"), Output("no_data_header", "style"), Output("data_page", "style"),
    Input("data_path", "modified_timestamp"), Input("force_refresh_data", "children"), State("data_path", "data"), State("project_title", "data"), State("cargar_cont", "children")
)
def load_data(ts, rf, datapath, title, buttons_ch):
    print(datapath)
    print(len(buttons_ch))
    single_button = dbc.Button("CARGAR", color="primary", className="me-1 mt-3 mb-3", id="cargar")
    double_button = [
            dbc.Button("CAMBIAR", color="primary", className="me-1 mt-3 mb-3", id="cargar"),
            dbc.Button("EDITOR", color="primary", className="me-1 mt-3 mb-3", id="editor_nav")
        ]
    if len(buttons_ch)==2:
        old_button = double_button
    else:
        old_button = single_button
    if ts is not None and datapath is not None:
        try:
            df = pd.DataFrame()
            df = pandas_load_wrapper(datapath)

            if df is not None:
                with open("dashboards/" + title) as json_file:
                    dash_data = json.load(json_file)

                dash_data["data_path"] = datapath

                with open("dashboards/" + title, "w") as outfile:
                    json.dump(dash_data, outfile)

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
                return dcc.Graph(figure=tabl,id="table"), "Archivo cargado: " + os.path.basename(datapath), double_button, None, None, {"display":"none"}, {"background-color":"lightgrey", "height":"auto"}
            else:
                print("df vacío")
                return dash.no_update, dash.no_update, old_button, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        except:
            print("error")
            return dash.no_update, dash.no_update, old_button, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    return dash.no_update, dash.no_update, single_button, {"display":"none"}, {"display":"none"}, None, {"background-color":"lightgrey", "height":"100%"}

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

            if df is not None:
                return df.to_dict("records")
        except:
            print("error")
        return dash.no_update