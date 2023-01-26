import codecs
import datetime
import json
from string import Template
import os

from pages.utils.buildCols import getColumns
from .makeCharts import findFunc
from inspect import signature


script_body_temp = '''
# -*- coding: utf-8 -*-
import json
from dash import Dash,html,Input,Output,dcc
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import os
import re
import pandas as pd

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
)

def pandas_load_wrapper(datapath):
    file_extension = os.path.splitext(os.path.basename(datapath))[1]
    print(file_extension)
    if file_extension == ".csv":
        df = pd.read_csv(datapath)
        df['index'] = range(1, len(df)+1)
        print(df.columns)
        return df
    elif re.match("^\.(xls|xlsx|xlsm|xlsb|odf|ods|odt)$$", file_extension):
        print('Excel')
        df = pd.read_excel(datapath)
        print(df)
        return df

df = pandas_load_wrapper("${data_path}")

app.layout = html.Div(
    [
        ${graphs}
    ],
    id="div",
    style={"margin": "0%", "height": "100vh", "width": "100vw", "background-color":"lightgray"}
)

if __name__ == "__main__":
    app.run(debug=True)
'''

def export_from_json(title):
    with open("dashboards/" + title) as json_file:
        dash_data = json.load(json_file)
    figures = []
    #Construir las figs
    if dash_data["contenedores"]: 
        for graph in dash_data["contenedores"]:
            if graph["figure"]:
                figure = graph["chart"] + "(data_frame=df,"
                params = []
                for key, val in graph["figure"].items():
                    if type(val) == list:
                        params.append(key + "=[" + ','.join(f'"{w}"' for w in val) + "]")
                    else:
                        params.append(key + "=\"" + val + "\"")
                figure = figure + ",".join(params) + ")"
                figures.append(figure)
    #Wrapper de dcc.Graph
    graphs = []
    index = 0
    for graph in dash_data["contenedores"]:
        if graph["style"]:
            fig = "dcc.Graph(figure=" + figures[index] + ", style={"
            styles = []
            for key, val in graph["style"].items():
                styles.append("\"" + key + "\":\"" + val + "\"")
            fig = fig + ",".join(styles) + "})"
        else:
            fig = "dcc.Graph(figure=" + figures[index] + ")"
        index+=1
        graphs.append(fig)

    script_body = Template(script_body_temp).substitute(graphs=",\n\t\t".join(graphs), data_path=dash_data["data_path"].replace("\\","/"))
    with codecs.open(str(get_download_path()) + "\\" + title.split(".")[0] + "_result.py", "w", "utf-8") as outfile:
        outfile.write(script_body)

def import_as_json(filename, data):
    print(data)
    print(len(data))
    print(type(data))

    if len(data)>0:
        title = filename
        result = {
            "id": title.split(".")[0],
            "data_path": "",
            "contenedores": [],
            "last_selected": "",
            "selected": ""
        }
        contenedores = []
        items = data.split('html.Div')
        for item in items:
            print(item)
            if "pandas_load_wrapper(\"" in item:
                data_index = item.find("pandas_load_wrapper(\"")+len("pandas_load_wrapper(\"")
                data_path = item[data_index:find_next_char(item, data_index, '\"')]
                result["data_path"] = data_path
            if "id=\"div\"" in item:
                item = item[item.find("[")+len("["):item.rfind("],")]
                print(item)
                div_items = item.split("dcc.Graph")
                id_count = 1
                for div_item in div_items[1::]:
                    div_item = div_item.strip()
                    div_item = div_item.replace(" ", "")
                    graph = div_item[div_item.find("(")+len("("):div_item.rfind(")")]
                    print("graphs=" + graph)
                    cont = {
                        "figure": {},
                        "chart": "",
                        "id": {
                            "index": id_count,
                            "type": "design-charts"
                        },
                        "style": {}
                    }
                    if "figure=" in graph:
                        selectChart = graph[graph.find("figure=")+len("figure="):graph.rfind("(")]
                        cont["chart"]=selectChart
                        sig = signature(findFunc(selectChart))
                        graph_data = graph[graph.find(selectChart + "(")+len(selectChart + "("):graph.rfind(")")]
                        #Conseguir los parámetros del gráfico
                        figure = {}
                        for param in sig.parameters.values():
                            if str(param).split("=")[0] in graph_data and str(param).split("=")[0] != "data_frame":
                                param_index = graph_data.find(str(param).split("=")[0] + "=")+len(str(param).split("=")[0] + "=")
                                if graph_data[param_index]=="[":
                                    values = graph_data[param_index+1:find_next_char(graph_data, param_index, ']')]
                                    values = values.replace("\"","")
                                    values = values.split(",")
                                else:
                                    values = graph_data[param_index+1:find_next_char(graph_data, param_index, '"')]
                                figure[str(param).split("=")[0]] = values
                        cont["figure"]=figure
                    #Conseguir los parámetros del style
                    if "style=" in graph:
                        style_data = graph[graph.find("style={")+len("style={"):graph.rfind("}")]
                        style_data = style_data.replace("'", "")
                        style_data = style_data.replace('"', "")
                        style_items = style_data.split(",")
                        style = {}
                        for style_item in style_items:
                            style_param = style_item.split(":")[0]
                            style_val = style_item.split(":")[1]
                            style[style_param] = style_val
                        cont["style"]=style
                    id_count+=1
                    contenedores.append(cont)
                result["contenedores"]=contenedores
        print("\n")
        print(result)
        #Actualizar historial de proyectos
        with open("assets/historial_proyectos.json") as json_file:
            historial = json.load(json_file)
        try:
            history_title = historial["projects"][result["id"]]
            return False
        except:
            historial["projects"][result["id"]] = {"date_created":datetime.datetime.now().__str__(), "last_opened":datetime.datetime.now().__str__()}
        
        with open("assets/historial_proyectos.json", "w") as outfile:
            json.dump(historial, outfile)

        #Crear json de dashboard
        with open("dashboards/"+result["id"]+".json", "w") as outfile:
            json.dump(result, outfile)

        return True
    return False

def find_next_char(string, start_index, target):
    if len(target) != 1:
        return None
    count = start_index + 1
    while count<len(string):
        if string[count] == target:
            return count
        count+=1
    return None


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')