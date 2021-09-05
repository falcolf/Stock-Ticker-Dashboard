import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(
                __name__, 
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/my_style.css"],
                update_title='Loading...',
                title='Equity Analytics'
                )

server = app.server
