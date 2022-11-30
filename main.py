from threading import Thread
from dash import Dash, html, page_container
import webview

app = Dash(__name__, external_stylesheets=["assets/css/bootstrap.min.css", "assets/css/style.css"], assets_folder='assets', assets_external_path="",
             assets_url_path="/assets", include_assets_files=True, serve_locally=True, use_pages=True)

app.layout = html.Div(
    [
        page_container
    ]
)

def run_app():
    app.run_server(port=8050, debug=False)

if __name__=='__main__':
    t = Thread(target=run_app)
    t.daemon = True
    t.start()
    window = webview.create_window("PDMAT", "http://127.0.0.1:8050/")
    webview.start(debug=True)