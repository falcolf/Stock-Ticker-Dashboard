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

from app import app
from utils.stock_data import get_stock_data


layout = html.Div([
                
                html.Div([
                    dbc.Row([
                                dbc.Col([
                                        dbc.FormGroup([
                                                        dbc.Label("Ticker"),
                                                        dbc.Input(placeholder="TCS.NS", type="text", id = 'ticker', value = 'TCS.NS'),
                                                        dbc.FormText("Enter Yahoo Finance Ticker"),
                                                        ]
                                                    )
                                    ], width={"size": 3, "offset": 1}),
                                dbc.Col([
                                        dbc.Label("Select Date Range"),
                                        dcc.DatePickerRange(
                                            id='date_range',
                                            initial_visible_month=datetime.date(2020, 4, 1),
                                            display_format='YYYY-MM-DD'
                                        )], width = 3),
                                dbc.Col([
                                        dbc.Button(
                                                    id='submit-button',
                                                    color = 'primary',
                                                    className="mr-1",
                                                    n_clicks=0,
                                                    children='Get Quote',
                                                    style={'fontSize':10}
                                                )], width = 4)
                                ], style = {"padding":"2rem 2rem 2rem 2rem"}),
                ]),
                html.Hr(),
                dcc.Graph(id='historical_values'),
                html.Hr(),
                dcc.Graph(id='earning_values')
            ])

@app.callback(
                Output('earning_values', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State('ticker','value'),
                 State('date_range', 'start_date'),
                 State('date_range', 'end_date')
                 ])
def publish_earnings_chart(nclicks, ticker, start_date, end_date):
    
    _, df = get_stock_data(ticker, start_date, end_date)
    traces = [
                go.Bar(x = df.index, y = df['Earnings'], name = 'Earnings'),
                go.Bar(x = df.index, y = df['Revenue'], name = 'Revenue')
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


@app.callback(
                Output('historical_values', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State('ticker','value'),
                 State('date_range', 'start_date'),
                 State('date_range', 'end_date')
                 ])
def publish_price_chart(nclicks, ticker, start_date, end_date):
    
    df, _ = get_stock_data(ticker, start_date, end_date)
    #traces = [go.Candlestick(x = df.index, y = df['Close'], mode = 'lines')]
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