import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from app import server
from apps import mkt_overview, custom_search, general_layouts


app.layout = html.Div([
                        dcc.Location(id='url', refresh=False),
                        general_layouts.navbar,
                        html.Div(id='page-content', children=[])
            ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/mkt_overview' or pathname == '/':
        return mkt_overview.layout
    if pathname == '/apps/custom_search':
        return custom_search.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
