import dash  # use Dash version 1.16.0 or higher for this app to work
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
print(dcc.__version__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

app.layout = html.Div([
    html.Br(),
    html.H1(children='Low Beta in Cryptocurrencies'),
    html.Br(),
    html.Div(children='''
        Interactive Dashboard
    ''', style={'fontFace': 'Arial', 'fontSize': 30}),
    html.Br(),

    html.Div([
    dcc.Checklist(
        id='check',
        options=[{'label': 'Cap Weighted', 'value': 'cap_weighted_index'},
                 {'label': 'Equal Weighted', 'value': 'ponderated_index'},
                 {'label': 'Minimum variance', 'value': 'MV'},
                 {'label': 'High Volatility', 'value': 'HV'},
                 {'label': 'Low Volatility', 'value': 'LV'},
                 {'label': 'Risk parity', 'value': 'RP'},
                 {'label': 'Low Beta', 'value': 'LB'},
                 {'label': 'High Beta', 'value': 'HB'},
                 ],
        value=['cap_weighted_index', 'ponderated_index'],
        labelStyle={'display': 'block'}
                  )],style={
        'color': "White"
    }),
    html.Br(),
    html.Div([
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None,
                  # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                  config={
                      'staticPlot': False,  # True, False
                      'scrollZoom': True,  # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': False,  # True, False
                      'displayModeBar': False,  # True, False, 'hover'
                      'watermark': False,
                      # 'modeBarButtonsToRemove': ['pan2d','select2d'],
                  },
                  className='six columns',
                  )
    ])
], style={

        'margin-left': 50 , 'margin-bottom':500
    })


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='check', component_property='value'),
)

def update_figure(value):
    dfCW  = pd.read_csv(r'data/processed/CW_20_price.csv')
    dfEW = pd.read_csv(r'data/processed/EW_20_price.csv')
    df = dfCW.merge(dfEW, on='date')
    dfMV = pd.read_csv(r'data/processed/MV_20_price.csv')
    df = df.merge(dfMV, on='date')
    dfLow_Vol = pd.read_csv(r'data/processed/Low_Vol_20_price.csv')
    df = df.merge(dfLow_Vol, on='date')
    dfHigh_Vol = pd.read_csv(r'data/processed/High_Vol_20_price.csv')
    df = df.merge(dfHigh_Vol, on='date')
    dfRP = pd.read_csv(r'data/processed/RP_20_price.csv')
    df = df.merge(dfRP, on='date')
    df.set_index('date', inplace=True)
    df.columns = ("cap_weighted_index", "ponderated_index", "MV", "LV", "HV", "RP")
    if len(value) > 0:
        fig = go.Figure()
        for val in value:
            df = df[value]
            fig.update_layout(font_color="White",
                margin=dict(l=50, r=20, t=20, b=20),
                paper_bgcolor="rgb(0,0,0,0)", plot_bgcolor="rgb(0,0,0,0)", colorway=['#0AF047', '#0EEEF0','#ffbf00','#cd9575','#4b5320', '#0EEEF0'], xaxis=dict(showgrid=False),
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


if __name__ == '__main__':
    app.run_server(debug=True)
