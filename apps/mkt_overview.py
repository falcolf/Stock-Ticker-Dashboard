from datetime import date
import datetime
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

from app import app
from utils.stock_data import get_stock_data, get_ticker_stats


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html as html_parser

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
options = webdriver.ChromeOptions()
options.add_argument('headless')

layout = html.Div([
                html.Div([
                            dcc.Interval(
                                    id='interval-component',
                                    interval=1000 * 1 * 60 * 60 * 6, # in milliseconds --> 6 hours
                                    n_intervals=0
                                ),
                            dbc.Row([
                                        dbc.Col(id = 'mmi_stats', width = 6),
                                        dbc.Col(dcc.Graph(id = 'world_indices'))
                                                
                                ], style = {"padding":"2rem 2rem 2rem 2rem"})              
                ]),
                html.Hr(),
                html.Div([
                            dbc.FormGroup([
                                            dbc.RadioItems(
                                                options=[
                                                    {'label': 'NIFTY', 'value': 'nifty'},
                                                    {'label': 'SENSEX', 'value': 'sensex'},
                                                ],
                                                value='nifty',
                                                id="index",
                                                inline = True,
                                                style = {"padding":"1rem 0.5rem 0.5rem 0.5rem"}
                                            ),
                                        ]),
                            dbc.Row(
                                    [
                                        dbc.Col(html.Div(dcc.Graph(id='index_performance'))),
                                        dbc.Col(html.Div(dcc.Graph(id = 'index_stats')), width=3),
                                    ]
                                )
                ])
                
            ])

@app.callback(
                [
                    Output('mmi_stats', 'children'),
                    Output('world_indices','figure')],
                [Input('interval-component', 'n_intervals')]
            )
def publish_top_stats(n):

    driver.get('https://www.tickertape.in/market-mood-index')
    html_src = html_parser.fromstring(driver.page_source)
    mmi_value = float(html_src.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/span')[0].text)

    mmi_indicator = daq.Gauge(
                    showCurrentValue=True,
                    color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,50],"orange":[50,70],"red":[70,100]}},
                    value=mmi_value,
                    label='MMI',
                    max=100,
                    min=0,
                )

    def get_ticker_change_fig(ticker, row, col):
        start, end, high, low = get_ticker_stats(ticker, period = '5d')
        return go.Indicator(
                        mode = "delta",
                        value = end,
                        title = {"text": "{}<br><span style='font-size:0.8em;color:gray'>5d Change</span>".format(ticker), 'font':{'size':15} },
                        delta = {'reference': start, 'relative': True, 'font':{'size':20}},
                        domain = {'row': row, 'column': col}
                    )
    

    world_indices = list()
    world_indices.append(get_ticker_change_fig(ticker = '^NSEI', row = 0, col = 0))
    world_indices.append(get_ticker_change_fig(ticker = '^BSESN', row = 0, col = 1))
    world_indices.append(get_ticker_change_fig(ticker = '^N225', row = 1, col = 0))
    world_indices.append(get_ticker_change_fig(ticker = 'LSEG.L', row = 1, col = 1))
    world_indices.append(get_ticker_change_fig(ticker = '^NDX', row = 2, col = 0))
    world_indices.append(get_ticker_change_fig(ticker = '^GSPC', row = 2, col = 1))

    world_indices_fig = {
                'data': world_indices,
                'layout': go.Layout(hovermode='closest', grid = {'rows': 3, 'columns': 2, 'pattern': "independent"}, height=400)
            }  

    return mmi_indicator, world_indices_fig


@app.callback(
                Output('index_stats', 'figure'),
                [Input('index', 'value')],
            )
def publish_stats(index):
    
    index_ticker = {
                    'nifty':'^NSEI',
                    'sensex':'^BSESN'
                }
    ticker = index_ticker.get(index)
    start, end, high, low = get_ticker_stats(ticker, period = '5d')

    traces = [go.Indicator(
                            mode = "number+delta",
                            value = end,
                            title = {"text": "{}<br><span style='font-size:0.8em;color:gray'>Current Value</span>".format(index)},
                            delta = {'reference': start, 'relative': True},
                            domain = {'x': [0.6, 1], 'y': [0, 1]})]
    fig = {
            'data': traces,
            'layout': go.Layout(hovermode='closest')
        }

    return fig

@app.callback(
                Output('index_performance', 'figure'),
                [Input('index', 'value')],
            )
def publish_price_chart(index):
    
    index_ticker = {
                    'nifty':'^NSEI',
                    'sensex':'^BSESN'
                }
    ticker = index_ticker.get(index)
    df, _ = get_stock_data(ticker, interval = '1wk')
    
    traces = [  
                go.Candlestick(
                                x=df.index,
                                open=df['Open'], 
                                high=df['High'],
                                low=df['Low'], 
                                close=df['Close']
                            )
                ]

    fig = {
            'data': traces,
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Price'},
                hovermode='closest'
            )
        }

    return fig