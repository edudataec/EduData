import codecs
import json
from string import Template
import os


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

    script_body = Template(script_body_temp).substitute(graphs=",\n\t\t".join(graphs), data_path=dash_data["data_path"])
    with codecs.open(str(get_download_path()) + "\\" + title.split(".")[0] + "_result.py", "w", "utf-8") as outfile:
        outfile.write(script_body)

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