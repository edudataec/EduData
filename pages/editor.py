import base64
import json
import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback, State, MATCH, ctx, ALL, clientside_callback
from pages.utils.export import export_from_json, import_as_json
from .utils.util import pandas_load_wrapper
from .utils.makeCharts import makeCharts, getOpts, parseSelections, makeDCC_Graph
from inspect import getmembers, isfunction
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

px_list = getmembers(px, isfunction)
chartOpts = [
    {"label":"Gráfico de área", "value":"px.area"},
    {"label":"Gráfico de barras", "value":"px.bar"},
    {"label":"Gráfico de barras polar", "value":"px.bar_polar"},
    {"label":"Gráfico de cajas", "value":"px.box"},
    {"label":"Gráfico cloroplético", "value":"px.choropleth"},
    {"label":"Mapa cloroplético", "value":"px.choropleth_mapbox"},
    {"label":"Gráfico de densidad de contorno", "value":"px.density_contour"},
    {"label":"Mapa de calor", "value":"px.density_heatmap"},
    {"label":"Gráfico ECDF", "value":"px.ecdf"},
    {"label":"Gráfico de embudo", "value":"px.funnel"},
    {"label":"Gráfico de area de embudo", "value":"px.funnel_area"},
    {"label":"Histograma", "value":"px.histogram"},
    {"label":"Gráfico de estalactita", "value":"px.icicle"},
    {"label":"Gráfico de líneas", "value":"px.line"},
    {"label":"Gráfico de líneas 3d", "value":"px.line_3d"},
    {"label":"Gráfico de líneas geográfico", "value":"px.line_geo"},
    {"label":"Gráfico de líneas polar", "value":"px.line_polar"},
    {"label":"Gráfico de categorías paralelas", "value":"px.parallel_categories"},
    {"label":"Pie chart", "value":"px.pie"},
    {"label":"Gráfico de dispersión", "value":"px.scatter"},
    {"label":"Gráfico de dispersión 3d", "value":"px.scatter_3d"},
    {"label":"Gráfico de dispersión geográfico", "value":"px.scatter_geo"},
    {"label":"Gráfico de dispersión polar", "value":"px.scatter_polar"},
    {"label":"Gráfico de matriz de dispersión", "value":"px.scatter_matrix"},
    {"label":"Diagrama ternario de dispersión", "value":"px.scatter_ternary"},
    {"label":"Gráfico de tiras", "value":"px.strip"},
    {"label":"Gráfico de rayos de sol", "value":"px.sunburst"},
    {"label":"Gráfico de línea de tiempo", "value":"px.timeline"},
    {"label":"Diagrama de árbol", "value":"px.treemap"},
    {"label":"Gráfico de violín", "value":"px.violin"},
]

offCanvStyle = {"borderRadius": "15px"}

dash.register_page(__name__, name='editor')

layout = html.Div(
    [
        dbc.NavbarSimple(
            [
                dbc.Container(
                    dcc.Link(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="assets/imgs/logo.svg", height="40px"))
                            ],
                            align="center",
                            className="g-0"
                        ),
                        href="/",
                        style={"text-decoration":"none"}
                    ) 
                ),
                dbc.NavItem(dbc.NavLink("Editor", href="/editor", active=True)),
                dbc.NavItem(dbc.NavLink("Data", href="/data"))
            ],
            color="primary",
            dark=True,
            links_left=True
        ),
        html.Div(id="load_json", hidden=True),
        html.Div(
            html.Div(
                [
                    html.Div(
                        id="design-area",
                        children=[],
                        style={
                            "backgroundColor": "#c5c6d0",
                            "position": "absolute",
                            "height": "100%",
                            "width": "100%",
                        },
                    ),
                    dcc.Graph(id={'index':'edit', 'type':"testFigure"}, style={"display": "none"}),
                    dbc.Offcanvas(
                        [
                            "Seleccione el tipo de gráfico y sus configuraciones",
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id={"index": "edit", "type": "selectChart_edit"},
                                        options=chartOpts,
                                        style={"width": "85%"}
                                    ),
                                    html.Img(
                                        id={"index": "edit", "type": "chartPreview_edit"},
                                        style={"width": "15%"}
                                    ),
                                ],
                                style={"display":"flex", "justify-content": "space-around", "align-items": "center"}
                            ),
                            dbc.Button(
                                id={"index": "edit", "type": "persistenceClear_edit"},
                                children="Limpiar Valores",
                                className="m-3",
                                color="info",
                                style={"visibility": "hidden"},
                            ),
                            dmc.Accordion(
                                id={"index": "edit", "type": "graphingOptions_edit"},
                            ),
                            dcc.Loading(
                                [
                                    dbc.Button(
                                        "Realizar Cambios",
                                        id={"index": "edit", "type": "submitEdits_edit"},
                                        className="m-3",
                                        style={"visibility": "hidden"},
                                    ),
                                ],
                                id="buttonLoading_edit",
                            ),
                        ],
                        id="chartDesignEditor",
                        style=offCanvStyle,
                    ),
                    dbc.Offcanvas(
                        [
                            "Seleccione el tipo de gráfico y sus configuraciones",
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id={"index": "2", "type": "selectChart_edit"}, options=chartOpts,
                                        style={"width": "85%"}
                                    ),
                                    html.Img(
                                        id={"index": "2", "type": "chartPreview_edit"},
                                        style={"width": "15%"}
                                    ),
                                ],
                                style={"display":"flex", "justify-content": "space-around", "align-items": "center"}
                            ),
                            dbc.Button(
                                id={"index": "2", "type": "persistenceClear_edit"},
                                children="Limpiar Valores",
                                className="m-3",
                                color="info",
                                style={"visibility": "hidden"},
                            ),
                            dmc.Accordion(
                                id={"index": "2", "type": "graphingOptions_edit"},
                            ),
                            dcc.Loading(
                                [
                                    dbc.Button(
                                        "Realizar Cambios",
                                        id={"index": "2", "type": "submitEdits_edit"},
                                        className="m-3",
                                        style={"visibility": "hidden"},
                                    )
                                ],
                                id="buttonLoading_edit2",
                            ),
                        ],
                        id="chartDesignEditor_edit",
                        style=offCanvStyle,
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "Abrir Modo Editor",
                                id="toggleEdit",
                                color="warning",
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Button(
                                id="openDesignEditor",
                                children="Añadir Gráfico",
                                n_clicks=0,
                                className="me-1",
                            ),
                            dbc.Button(
                                id="saveLayout",
                                children="Guardar",
                                n_clicks=0,
                                className="me-1",
                                color="success",
                            ),
                        ],
                        id="edit_buttons_holder",
                        style={"zIndex": "1", "position": "absolute", "width": "100%"},
                    ),
                    dbc.Button(id="editActive", style={"display": "none"}),
                    dbc.Button(id="syncStore", style={"display": "none"}),
                    dbc.Button(id="deleteTarget", style={"display": "none"}),
                ],
                id="design-holder",
            ), style={"margin": "0%", "height": "100%", "width": "100%"}
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
                        dcc.Upload(dbc.Button("IMPORTAR", id="imp_button"), id="imp_button_upload"),
                        dbc.Button("EXPORTAR", id="exp_button")
                    ],
                    className="slider-opt-cont"
                ),
            ],
            id="options-slider-cont",
            className="options-slider-cont-up"
        ),
        html.Div(
            id="hideLayout",
            n_clicks=0,
            className="hide btn-light fa-solid fa-eye",
        ),
        html.Div(id="save_json")
    ]
)

@callback(
    Output("chartEditor", "is_open"),
    Input("openEditor", "n_clicks"),
    State("chartEditor", "is_open"),
    prevent_initial_call=True,
)
@callback(
    Output("chartDesignEditor", "is_open"),
    Input("openDesignEditor", "n_clicks"),
    State("chartDesignEditor", "is_open"),
    prevent_initial_call=True,
)
@callback(
    Output("sidebar", "is_open"),
    Input("sidebarButton", "n_clicks"),
    State("sidebar", "is_open"),
    prevent_initial_call=True,
)
def openEditor(n1, isOpen):
    if n1 > 0:
        return not isOpen
    return isOpen

@callback(
    Output("chartDesignEditor_edit", "is_open"),
    Output({"type": "selectChart_edit", "index": "2"}, "value"),
    Input("editActive", "n_clicks"),
    State("chartDesignEditor_edit", "is_open"),
    State("focused-graph", "data"),
    State("figures", "data"),
    prevent_initial_call=True,
)
def openEditor_edit(n1, isOpen, id, figs):
    if n1 > 0:
        for f in figs:
            if f["id"] == json.loads(id):
                chart = f["chart"]
        return not isOpen, chart
    return isOpen

@callback(
    Output({"type": "graphingOptions_edit", "index": MATCH}, "children"),
    Output({"type": "persistenceClear_edit", "index": MATCH}, "style"),
    Output({"type": "submitEdits_edit", "index": MATCH}, "style"),
    Output({"type":"chartPreview_edit", "index": MATCH}, "src"),
    Input({"type": "selectChart_edit", "index": MATCH}, "value"),
    State("dataInfo", "data"),
    Input({"index": MATCH, "type": "persistenceClear_edit"}, "n_clicks"),
    State("focused-graph", "data"),
    State("figures", "data"),
    prevent_initial_call=True,
)
def graphingOptions_edit(chart, data, p, id, figs):
    if chart:
        if not data:
            print("No ha cargado un set de datos")
            return (
                "No ha cargado un set de datos",
                {"visibility": "hidden"},
                {"visibility": "hidden"},
                ""
            )
        df = pd.DataFrame.from_dict(data)
        try:
            if ctx.triggered_id["type"] == "selectChart_edit":
                return (
                    getOpts(chart, id, figs, df),
                    {"visibility": True},
                    {"visibility": True},
                    "assets/imgs/" + chart + ".png"
                )
        except:
            ...
        return getOpts(chart, None, "bruh", df), {"visibility": True}, {"visibility": True}, "assets/imgs/" + chart + ".png"
    return "Escoger una opción", {"visibility": "hidden"}, {"visibility": "hidden"}, ""

@callback(
    Output("design-area", "children"),
    Output("figures", "data"),
    Output({"type": "submitEdits_edit", "index": ALL}, "children"),
    Input({"type": "submitEdits_edit", "index": ALL}, "n_clicks"),
    Input("deleteTarget", "n_clicks"),
    Input("figureStore", "data"),
    Input("load_json", "children"),
    State("dataInfo", "data"),
    State({"type": "graphingOptions_edit", "index": ALL}, "children"),
    State({"type": "selectChart_edit", "index": ALL}, "value"),
    State("design-area", "children"),
    State("focused-graph", "data"),
    State("figures", "data"),
    State("project_title", "data")
)
def updateLayout(n1, d1, figs, load, data, opts, selectChart, children, target, figouts, title):
    btn = ["Realizar Cambios"] * len(n1)
    if data:
        df = pd.DataFrame.from_dict(data)
        df = df.infer_objects()
        if ctx.triggered_id == "load_json":
            with open("dashboards/" + title) as json_file:
                dash_data = json.load(json_file)
            children = [makeDCC_Graph(df, i) for i in dash_data['contenedores']]
            return children, dash_data['contenedores'], btn
        if ctx.triggered_id == "figureStore":
            children = [makeDCC_Graph(df, i) for i in figs]
            return children, figs, btn
        if data and opts and ctx.triggered_id != "deleteTarget":
            if len(children) == 0:
                figouts = []
            trig = ctx.triggered_id.index

            if trig == "edit":
                opts = opts[0]
                figureDict = parseSelections(
                    opts[0]["props"]["children"][1]["props"]["children"],
                    opts[1]["props"]["children"][1]["props"]["children"],
                )
                figureDict["chart"] = selectChart[0]

                used = []
                for child in children:
                    used.append(child["props"]["id"]["index"])

                y = 0
                while y < 1000:
                    if y not in used:
                        break
                    y += 1

                figureDict["id"] = {"index": y, "type": "design-charts"}

                if not "style" in figureDict:
                    figureDict["style"] = {
                        "position": "absolute",
                        "width": "40%",
                        "height": "40%",
                    }

                children.append(makeDCC_Graph(df, figureDict))
                figouts.append(figureDict)
                return children, figouts, btn
            else:
                opts = opts[1]
                figureDict = parseSelections(
                    opts[0]["props"]["children"][1]["props"]["children"],
                    opts[1]["props"]["children"][1]["props"]["children"],
                )
                figureDict["chart"] = selectChart[1]
                figureDict["id"] = json.loads(target)

                children = children.copy()

                for c in range(len(children)):
                    if children[c]["props"]["id"] == json.loads(target):
                        if "figure" in children[c]["props"]:
                            children[c]["props"]["figure"] = makeCharts(df, figureDict)[
                                0
                            ]
                        else:
                            figureDict["style"] = {
                                "position": "absolute",
                                "width": "40%",
                                "height": "40%",
                            }
                            children[c] = makeDCC_Graph(df, figureDict)
                figouts = figouts.copy()
                for f in range(len(figouts)):
                    if figouts[f]["id"] == json.loads(target):
                        figouts[f] = figureDict
                        figouts[f]["id"] = json.loads(target)

                return children, figouts, btn

        elif ctx.triggered_id == "deleteTarget":
            for c in range(len(children)):
                if children[c]["props"]["id"] == json.loads(target):
                    del children[c]
                    break
            for fig in figouts:
                if fig["id"] == json.loads(target):
                    figouts.remove(fig)

            return children, figouts, btn
    raise PreventUpdate

@callback(
    Output("alert", "children"),
    Output("statusAlert", "is_open"),
    Output("alert", "className"),
    Input("exp_button", "n_clicks"),
    Input("imp_button_upload", "contents"),
    Input("figureStore", "data"),
    State("project_title", "data"),
    State("imp_button_upload", "filename"),
    prevent_initial_call = True
)
def save_json(n, contents, figures, title, filename):
    print(figures)
    if ctx.triggered_id == "exp_button":
        if n>0:
            export_from_json(title)
            return 'Se exportó el dashboard en la carpeta de descargas', True, "alert-success"
    elif ctx.triggered_id == "imp_button_upload":
        if contents is not None and filename!="":
            file_end = filename.split(".")[1]
            title = filename.split(".")[0]
            if file_end != "py":
                return 'No se seleccionó un script de Python.', True, "alert-danger"
            try:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                if import_as_json(filename, decoded.decode('utf-8')):
                    return 'Se importó el archivo correctamente, con el nombre:' + title, True, "alert-success"
                else:
                    return 'Error cargando el script seleccionado', True, "alert-danger"
            except:
                return 'Error importando el script seleccionado', True, "alert-danger"
        else:
            raise PreventUpdate
    elif figures is not None:
        with open("dashboards/" + title) as json_file:
            dash_data = json.load(json_file)
    
        dash_data["contenedores"] = figures

        with open("dashboards/" + title, "w") as out_file:
            json.dump(dash_data, out_file)
        return 'Se ha grabado el dashboard', True, "alert-success"
    raise PreventUpdate

#Options callbacks
@callback(Output("options-slider-cont", "className"), Input("slider-button", "n_clicks"), State("options-slider-cont", "className"))
def slide_down(n_clicks, className):
    if className == "options-slider-cont-up":
        return "options-slider-cont-down"
    elif className == "options-slider-cont-down":
        return "options-slider-cont-up"

@callback(Output("edit_buttons_holder", "style"), Output("options-slider-cont", "style"), Output("hideLayout", "className"), Input("hideLayout", "n_clicks"), State("hideLayout", "className"))
def hide_buttons(n, classN):
    if n>0 :
        if classN == "hide btn-light fa-solid fa-eye":
            return {"display":"none"}, {"display":"none"}, "hide btn-light fa-solid fa-eye-slash"
        else:
            return {"zIndex": "1", "position": "absolute", "width": "100%"}, {}, "hide btn-light fa-solid fa-eye"
