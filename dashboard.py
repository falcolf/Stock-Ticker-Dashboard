from datetime import date
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from stock_data import get_stock_data

app = dash.Dash()

app.layout = html.Div([
                
                html.Div([
                    html.H1('Stock Analysis Dashboard', style = {'textAlign':'center'}),
                    html.H5('Developed by Parth Agarwal', style = {'textAlign':'center'})
                ]),
                html.Div([
                    html.Div(dcc.Input(
                                id = 'ticker', 
                                type = 'text', 
                                placeholder = 'Yahoo Finance Stock Ticker',
                                style = {'width':'90%', 'height':'50px'}
                            ), style = {'display':'inline-block', 'padding-right':'50px', 'width':'30%'}),
                    dcc.DatePickerRange(
                                id='date_range',
                                initial_visible_month=date(2020, 4, 1),
                                display_format='YYYY-MM-DD',
                                style = {'display':'inline-block','width':'30%'}
                            ),
                    html.Button(
                                id='submit-button',
                                n_clicks=0,
                                children='Submit',
                                style={'fontSize':20}
                            )
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
    #return "{},{},{},{}".format(nclicks,ticker,start_date,end_date)
    #_, df = get_stock_data('TCS.NS', '2019-04-01','2021-03-31')
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


if __name__ == "__main__":
    app.run_server()