import json
from threading import Thread
from dash import Dash, html, page_container, dcc, Output, Input, State, ALL, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import webview

app = Dash(__name__, external_stylesheets=["assets/css/bootstrap.min.css", "assets/css/style.css", dbc.icons.FONT_AWESOME], external_scripts=["assets/js/custom.js", "assets/js/jquery.min.js"], assets_folder='assets', assets_external_path="",
             assets_url_path="/assets", include_assets_files=True, use_pages=True)

app.layout = html.Div(
    [
        dcc.Store(id="data_path", storage_type="session"),
        dcc.Store(id="project_title", storage_type="session"),
        dcc.Store(id="selected_cont_index", storage_type="session"),
        dbc.Modal(
            id="statusAlert",
            children=[html.Div(id="alert", className="alert-success")],
            is_open=False,
            centered=True,
        ),
        dbc.Modal(
            id="statusAlertData",
            children=[html.Div(id="alertData", className="alert-success")],
            is_open=False,
            centered=True,
        ),
        dbc.Modal(
            id="statusAlertDashboard",
            children=[html.Div(id="alertDashboard", className="alert-danger")],
            is_open=False,
            centered=True,
        ),
        dcc.Store(id="dataInfo", data=[], storage_type="session"),
        dcc.Store(id="figureStore", data=[], storage_type="session"),
        dcc.Store(id="focused-graph", storage_type="session"),
        dcc.Store(id="figures", storage_type="session", data=[]),
        html.Div(id="persistenceClear"),
        page_container
    ]
)

app.clientside_callback(
    """
        function (n1, c) {
            if (n1 > 0) {
                $('#design-area .dash-graph').unbind()
                $('#design-area .dash-graph > div:first-of-type').empty()
                $('#design-area .dash-graph').on('mouseenter', function () {
                    sessionStorage.setItem('focused-graph',$(this)[0].id)
                    $('#design-area .dash-graph').removeClass('focused-graph')
                    $(this).addClass('focused-graph')
                })
                if (c == 'edit') {
                    $("#design-holder").removeClass('edit')
                    return ['','Abrir Modo Editor']
                }
                $("#design-holder").addClass('edit')
                $('#design-area .dash-graph').each(function() {
                    addEditButtons($(this).find('div')[0])
                    dragElement($(this).find('.fa-up-down-left-right')[0])
                })
                return ['edit','Cerrar Modo Editor']
            }
            return [window.dash_clientside.no_update,window.dash_clientside.no_update]
        }
    """,
    Output("design-area", "className"),
    Output("toggleEdit","children"),
    Input("toggleEdit", "n_clicks"),
    State("design-area", "className")
)

app.clientside_callback(
    """
    async function saveLayout(n1) {
        const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id);
        if (n1 > 0) {
            figures = JSON.parse(sessionStorage.getItem('figures'))
            figureData = []
            children = $("#design-area").children()
            ref = $("#design-area")[0].getBoundingClientRect()
            for (y=0; y < figures.length; y++) {
                for (x=0; x < children.length; x++) {
                    if (JSON.stringify(figures[y].id) == children[x].id) {
                        styling = children[x].style.cssText.split('; ')
                        style = {}
                        for (z=0; z<styling.length;z++) {
                            if (styling[z].split(': ')[1].split(';')[0].includes('px')) {
                                if (['height', 'top'].includes(styling[z].split(':')[0])) {
                                    adj = (parseFloat(styling[z].split(': ')[1].split(';')[0]) / ref.height)*100 + '%'
                                } else {
                                    adj = (parseFloat(styling[z].split(': ')[1].split(';')[0]) / ref.width)*100 + '%'
                                }
                                style[styling[z].split(':')[0]] = adj
                            } else {
                                style[styling[z].split(':')[0]] = styling[z].split(': ')[1].split(';')[0]
                            }
                        }
                        figures[y]['style'] = style
                        break
                    }
                }
                figureData.push(figures[y])
            }
            return [figureData, window.dash_clientside.no_update]
        }
        console.log('load json')
        return [window.dash_clientside.no_update, 1]
    }
    """,
    Output("figureStore", "data"),
    Output("load_json", "children"),
    Input("saveLayout", "n_clicks"),
)

app.clientside_callback(
    """function () {
        const keys = Object.keys(sessionStorage)
        const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id);
        if (typeof oldTrig !== 'undefined') {
            if (oldTrig == triggered) {
                return ''
            }
        }
        oldTrig = triggered
        for (let key of keys) {
            if (String(key).includes('_dash_persistence') && !String(key).includes('template')) {
                sessionStorage.removeItem(key)
            }
        }
        return ''
    }""",
    Output("persistenceClear", "children"),
    Input("preloadData", "value"),
    Input({"index": ALL, "type": "persistenceClear"}, "n_clicks"),
)

app.clientside_callback(
    """function dragging(d) {
        setTimeout(function () {
        $('#design-area .dash-graph').unbind()
        $('#design-area .dash-graph').on('mouseenter', function () {
            sessionStorage.setItem('focused-graph',$(this)[0].id)
            $('#design-area .dash-graph').removeClass('focused-graph')
            $(this).addClass('focused-graph')
        })
        $('#design-area .dash-graph > div:first-of-type').empty()
        $('#design-area.edit .dash-graph').each(function() {
            addEditButtons($(this).find('div')[0])
            dragElement($(this).find('.fa-up-down-left-right')[0])
        })}, 300)
        
        return window.dash_clientside.no_update
    }""",
    Output("design-area", "id"),
    Input("design-area", "children"),
)

app.clientside_callback(
    """
        function (n1) {
            if (n1 > 0) {
                return sessionStorage.getItem('focused-graph')
            }
            return ''
        }
    """,
    Output("focused-graph", "data"),
    Input("syncStore", "n_clicks"),
    prevent_initial_call=True,
)

def run_app():
    app.run_server(port=8050, debug=False)

if __name__=='__main__':
    t = Thread(target=run_app)
    t.daemon = True
    t.start()
    window = webview.create_window("PDMAT", "http://127.0.0.1:8050/")
    webview.start(debug=True)