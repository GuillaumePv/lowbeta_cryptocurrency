import dash  # use Dash version 1.16.0 or higher for this app to work
import os
import sys
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_table
from dash_table.Format import Format, Scheme
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
from pathlib import Path

## Absolute path to use in all file
path_original = Path(__file__).resolve().parents[0]
path_data_processed = (path_original / "../data/processed/").resolve()
path_data_strat = (path_original / "../data/strats/").resolve()

# set up path variable
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import config as c
marketcap = format(c.market_cap,'.0e')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

app.layout = html.Div([
    html.Br(),
    html.H1(children='Low Beta in Cryptocurrencies Interactive Dashboard'),
    html.Br(),
    html.Div(children='''
         Log-Performance for 100-cryptocurrency portfolios
    ''', style={'fontFace': 'Arial', 'fontSize': 30}),
    html.Br(),
    html.Div([
    dcc.Checklist(
        id='check',
        options=[{'label': '  Cap Weighted', 'value': 'cap_weighted_index'},
                 {'label': '  BTC', 'value': 'BTC'},
                 {'label': '  Equal Weighted', 'value': 'ponderated_index'},
                 {'label': '  Minimum Variance', 'value': 'MV'},
                 {'label': '  High Volatility', 'value': 'HV'},
                 {'label': '  Low Volatility', 'value': 'LV'},
                 {'label': '  Low Beta', 'value': 'LB'},
                 {'label': '  High Beta', 'value': 'HB'},
                 {'label': '  Low Beta EW', 'value': 'LB_EW'},
                 {'label': '  High Beta EW', 'value': 'HB_EW'},
                 {'label': '  Low Beta BTC', 'value': 'LB_BTC'},
                 {'label': '  High Beta BTC', 'value': 'HB_BTC'},
                 ],
        value=['cap_weighted_index', 'ponderated_index'],
        labelStyle={'display': 'inline-block', 'padding':'1em', 'background-color':'#0c1f4c'}
                  )],style={
        'color': "White", 'fontSize':18}),
    html.Br(),
    html.Div([
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                  config={
                      'staticPlot': False,  # True, False
                      'scrollZoom': True,  # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,  # True, False
                      'displayModeBar': False,  # True, False, 'hover'
                      'watermark': False,
                  },
                  className='six columns',)
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(children='''
        Metrics Table
    ''', style={'fontFace': 'Arial', 'fontSize': 30}),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': '20 Crypto Model', 'value': 'metrics1.csv'},
                {'label': '100 Crypto Model', 'value': 'metrics2.csv'}
            ],value='metrics1.csv',
        )],style = {'margin-right': 1100, 'color':'black', 'backgroundColor':'black'}),
    html.Br(),
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=(),
            data=[],
    style_cell={'textAlign': 'right', 'fontSize':16, 'font-family':'arial', 'minWidth': '120px', 'width': '120px', 'maxWidth': '120px'},
    style_header={
        'backgroundColor': 'rgb(0, 0, 0, 0)',
        'color': 'lime',
        'border': '0px solid blue',
        'fontSize':16
    },
    style_data={
        'backgroundColor': 'rgb(0, 0, 0, 0)',
        'color': 'turquoise',
        'border': '0px solid blue',
    },
    style_data_conditional=[
        {
            'if': {
                'column_id': 'Portfolio',
            },
            'textAlign': 'left',
            'minWidth': '180px'
        },],

            sort_action='native')
    ], style={
        'margin-right': 100 , 'margin-left':10, 'margin-bottom':0, 'fontFace': 'Arial'
    }),
], style={
        'margin-left': 50 , 'margin-bottom':500
    })

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='check', component_property='value'),
)

def update_figure(value):
    df = pd.read_csv(f'data/strats/all_price_{c.number_cryptos}_1e{marketcap[-1]}.csv')
    #this part is to set the graph length
    df.set_index('datetime', inplace=True)
    df = np.log(df) #take logs of the data
    #########################################
    if len(value) > 0:
        fig = go.Figure()
        for val in value:
            df = df[value]
            fig.update_layout(font_color="White",
                margin=dict(l=50, r=20, t=20, b=20),
                paper_bgcolor="rgb(0,0,0,0)", plot_bgcolor="rgb(0,0,0,0)", colorway=['#0AF047', '#0EEEF0','#ffbf00','#cd9575','#4b5320', '#5D8AA8', '#F0F8FF', '#915C83', '#FF9966', '#007FFF', '#848482', '#EBCDFF'], xaxis=dict(showgrid=False),
     yaxis=dict(showgrid=False)
            )
            fig.add_trace(go.Scatter(x=df.index, y=df[val],
                    mode='lines',
                    name=val))
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(font_color="White",
                          margin=dict(l=50, r=20, t=20, b=20),
                          paper_bgcolor="rgb(0,0,0,0)", plot_bgcolor="rgb(0,0,0,0)", colorway=['#0AF047', '#0AEEF0']
                          )
        return fig


@app.callback(
    Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data'),
    Input(component_id='dropdown', component_property='value'),
)

def update_output(val):
    df3 = pd.read_csv(f'data/processed/df_metrics_20_1e{marketcap[-1]}.csv')
    df4 = pd.read_csv(f'data/processed/df_metrics_100_1e{marketcap[-1]}.csv')
    df3.rename(columns = {'Unnamed: 0':'Strategies'}, inplace = True)
    df4.rename(columns = {'Unnamed: 0':'Strategies'}, inplace = True)

    if val == "metrics1.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=3, scheme=Scheme.fixed), "type":'numeric'} for i in df3.columns]
        data=df3.to_dict('records')
        return columns, data
    elif val == "metrics2.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=3, scheme=Scheme.fixed), "type":'numeric'} for i in df4.columns]
        data=df4.to_dict('records')
        return columns, data
    elif val == "metrics3.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=3, scheme=Scheme.fixed), "type":'numeric'} for i in df5.columns]
        data=df4.to_dict('records')
        return columns, data

if __name__ == '__main__':
    app.run_server(debug=True)
