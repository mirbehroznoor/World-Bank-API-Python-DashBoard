from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

import webbrowser
from threading import Timer

from appPages import simpleApp, multiApp


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, suppress_callback_exceptions=True)
# MATERIA
# LUMEN
# SANDSTONE

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.MATERIA]
           )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update the index


@ callback(Output('page-content', 'children'),
           [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/multiApp':
        return multiApp.layout
    elif pathname == '/simpleApp':
        return simpleApp.layout
    else:
        return multiApp.layout
    # You could also return a 404 "URL not found" page here


# port = 8050


def open_browser():
    webbrowser.open_new("localhost:8050")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=8050, use_reloader=False)
