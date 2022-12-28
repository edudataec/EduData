import json
import dash
from dash import Dash, dcc, Output, Input, html, page_container, callback, State, MATCH, ctx, ALL, clientside_callback
from .utils.util import pandas_load_wrapper
from .utils.makeCharts import makeCharts, getOpts, parseSelections, makeDCC_Graph
from inspect import getmembers, isfunction
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

px_list = getmembers(px, isfunction)
chartOpts = ["px." + i for i, y in px_list]  # +['go.'+i for i, y in go_list]
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
                            "Select the chart type and options below",
                            dcc.Dropdown(
                                id={"index": "edit", "type": "selectChart_edit"},
                                options=chartOpts,
                            ),
                            dbc.Button(
                                id={"index": "edit", "type": "persistenceClear_edit"},
                                children="Clear All Values",
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
                                        "Make Changes",
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
                            "Select the chart type and options below",
                            dcc.Dropdown(
                                id={"index": "2", "type": "selectChart_edit"}, options=chartOpts
                            ),
                            dbc.Button(
                                id={"index": "2", "type": "persistenceClear_edit"},
                                children="Clear All Values",
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
                                        "Make Changes",
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
                                "Toggle Edit Mode",
                                id="toggleEdit",
                                color="warning",
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Button(
                                id="openDesignEditor",
                                children="Add Chart",
                                n_clicks=0,
                                className="me-1",
                            ),
                            dbc.Button(
                                id="saveLayout",
                                children="Save Layout",
                                n_clicks=0,
                                className="me-1",
                                color="success",
                            ),
                            dbc.Button(
                                id="exportLayout",
                                children="Export Layout",
                                n_clicks=0,
                                className="me-1",
                                color="info",
                            ),
                            dcc.Download(id="layoutDownload")
                        ],
                        style={"zIndex": "1", "position": "absolute", "width": "100%"},
                    ),
                    dbc.Button(id="editActive", style={"display": "none"}),
                    dbc.Button(id="syncStore", style={"display": "none"}),
                    dbc.Button(id="deleteTarget", style={"display": "none"}),
                ],
                id="design-holder",
            ), style={"margin": "1%", "height": "98%", "width": "98%"}
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
    Input({"type": "selectChart_edit", "index": MATCH}, "value"),
    Input("dataInfo", "data"),
    Input({"index": MATCH, "type": "persistenceClear_edit"}, "n_clicks"),
    State("focused-graph", "data"),
    State("figures", "data"),
    prevent_initial_call=True,
)
def graphingOptions_edit(chart, data, p, id, figs):
    if chart:
        if not data:
            print("Please load a dataset")
            return (
                "Please load a dataset",
                {"visibility": "hidden"},
                {"visibility": "hidden"},
            )
        df = pd.DataFrame.from_dict(data)
        try:
            if ctx.triggered_id["type"] == "selectChart_edit":
                return (
                    getOpts(chart, df, id, figs),
                    {"visibility": True},
                    {"visibility": True},
                )
        except:
            ...
        return getOpts(chart, df), {"visibility": True}, {"visibility": True}
    return "Please select an option", {"visibility": "hidden"}, {"visibility": "hidden"}

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
    btn = ["Make Changes"] * len(n1)
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

'''@callback(
    Output("figureStore", "data"),
    Input("load_json", "n_clicks"),
    State("project_title", "data"),
)
def load_json(n1,title):
    triggered = ctx.triggered_id
    if triggered == "load_json":
        with open("dashboards/"+title) as json_file:
            dash_data = json.load(json_file)

        return dash_data["contenedores"]'''

@callback(
    Output("alert", "children"),
    Output("statusAlert", "is_open"),
    Input("figureStore", "data"),
    State("project_title", "data"),
)
def save_json(figures, title):
    print(figures)
    if figures is not None:
        with open("dashboards/" + title) as json_file:
            dash_data = json.load(json_file)
    
        dash_data["contenedores"] = figures

        with open("dashboards/" + title, "w") as out_file:
            json.dump(dash_data, out_file)
        return 'Se ha grabado el dashboard', True
    raise PreventUpdate
