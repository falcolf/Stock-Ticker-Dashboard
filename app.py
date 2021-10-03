import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_auth

app = dash.Dash(
                __name__, 
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/style.css", "https://codepen.io/chriddyp/pen/bWLwgP.css"],
                update_title='Loading...',
                title='Equity Analytics'
                )

username_pass_pairs = [['admin','pass']]
auth = dash_auth.BasicAuth(app, username_pass_pairs)

server = app.server
