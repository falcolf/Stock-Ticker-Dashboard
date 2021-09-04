from datetime import date
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
options = webdriver.ChromeOptions();
options.add_argument('headless');

driver.get('https://www.tickertape.in/market-mood-index')
html_src = html_parser.fromstring(driver.page_source)
mmi_value = float(html_src.xpath('//*[@id="app-container"]/div/div[1]/div[1]/div/div[2]/span')[0].text)


layout = html.Div([
                html.Div([
                            daq.Gauge(
                                showCurrentValue=True,
                                color={"gradient":True,"ranges":{"green":[0,30],"yellow":[30,50],"orange":[50,70],"red":[70,100]}},
                                value=mmi_value,
                                label='MMI',
                                max=100,
                                min=0,
                            ),
                            dcc.Graph(id = 'index_stats')              
                ]),
                html.Div([
                            dcc.RadioItems(
                                id = 'index',
                                options=[
                                    {'label': 'NIFTY', 'value': 'nifty'},
                                    {'label': 'SENSEX', 'value': 'sensex'},
                                ],
                                value='nifty',
                                labelStyle={'display': 'inline-block'}
                            ),
                            html.Hr(),
                            dcc.Graph(id='index_performance') 
                ])
                
            ])

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