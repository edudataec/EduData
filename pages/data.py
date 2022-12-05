import dash
import os
from dash import Dash, dcc, Output, Input, State, html, page_container, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import re

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
                dbc.NavItem(dbc.NavLink("Data", href="/data", active=True)),
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
                        html.H2(id="nombre_archivo", className="mt-3"),
                        html.Div(dash_table.DataTable(id="full_data_table"), style={"display":"none"}),
                        dbc.Row(
                            dbc.Col(
                                [
                                    dash_table.DataTable(id="table", 
                                    page_current=0, page_size=20, page_action='custom',
                                    sort_action='custom', sort_mode='multi', sort_by=[])
                                ],
                                id="table_cont",
                                class_name="mt-3",
                                width="auto"
                            ),
                            justify="end"
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.Div(dbc.Button("CAMBIAR", color="primary", className="me-1 mt-3 mb-3", id="cambiar"), id="cambiar_cont"),
                                    html.Div(id="button_func_enabler", style={"display":"none"}),
                                    html.Div(id="cambiar_target")
                                ],
                                width="auto"
                            ),
                            justify="end"
                        ),
                    ],
                    align="center",
                    width="auto"
                )
            ],
            align="center",
            justify="center",
            style={"background-color":"lightgrey", "height":"auto"}
        )
    ]
)

@callback(Output("nombre_archivo", "children"), Input("data_path", "modified_timestamp"), State("data_path", "data"))
def update_title(ts, data):
    print(ts)
    if ts is not None:
        print(data)
        return "Archivo cargado: " + os.path.basename(data)

@callback(Output("table", "columns"), Output("full_data_table", "columns"), Output('full_data_table', 'data'),Input("data_path", "modified_timestamp"), State("data_path", "data"))
def load_update_data(ts, datapath):
    if ts is not None:
        df = pd.DataFrame()
        file_extension = os.path.splitext(os.path.basename(datapath))[1]
        print(file_extension)
        try:
            if file_extension == ".csv":
                df = pd.read_csv(datapath)
                df['index'] = range(1, len(df)+1)
                print(df.columns)
            elif re.match("^\.(xls|xlsx|xlsm|xlsb|odf|ods|odt)$", file_extension):
                print('Excel')
                df = pd.read_excel(datapath)
                print(df)
        except:
            print("error")
        columns = [{'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)]
        return columns, columns, df.to_dict('records')

@callback(Output('table', 'data'), 
Input('table', 'page_current'), Input('table', 'page_size'), Input('table', 'sort_by'), Input('full_data_table', 'data'))
def load_update_data(page_current, page_size, sort_by, data):
    print(sort_by)
    df = pd.DataFrame.from_records(data)
    if len(sort_by):
        dff = df.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        dff=df
    return dff.iloc[page_current*page_size:(page_current + 1)*page_size].to_dict('records')
