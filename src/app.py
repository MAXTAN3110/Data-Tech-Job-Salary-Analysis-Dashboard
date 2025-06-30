import dash
from dash import Dash, html, dcc, _dash_renderer
from callbacks.server_callbacks import register_server_callbacks
from callbacks.client_callbacks import register_client_callbacks
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from components.navbar import create_navbar

_dash_renderer._set_react_version("18.2.0")

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dmc.styles.ALL],
    external_scripts=[
        "https://d3js.org/d3.v7.min.js",
        "/assets/donutChart.js",
        "https://code.iconify.design/2/2.2.1/iconify.min.js",
    ],
    use_pages=True,
)
server = app.server


app.layout = dmc.MantineProvider(
    [
        dcc.Store(id="store"),
        dcc.Location(id="url", refresh=False),
        create_navbar(),
        dash.page_container,
    ]
)

register_server_callbacks(app)
register_client_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, dev_tools_ui=True, port=8051)
