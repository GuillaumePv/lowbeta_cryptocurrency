import dash  # use Dash version 1.16.0 or higher for this app to work
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dash_table
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

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
        options=[{'label': 'Cap Weighted', 'value': 'cw_portfolio'},{'label': 'Equal Weighted', 'value': 'ew_portfolio'}],
        value=['cw_portfolio', 'ew_portfolio'],
        labelStyle={'display': 'block'}
                  )],style={
        'color': "White"
    }),
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
                  className='six columns',
                  )
    ]),
], style={

        'margin-left': 50 , 'margin-bottom':500
    })


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='check', component_property='value'),
)

def update_figure(value):
    dfCW  = pd.read_csv(r'CW_20_price.csv')
    dfEW = pd.read_csv(r'EW_20_price.csv')
    df = dfCW.merge(dfEW, on='date')
    df.set_index('date', inplace=True)
    
    
    returns_price_CW = pd.Series.to_frame(df.iloc[:,0]/df.iloc[:,0].shift(1).replace(np.nan, 0))
    returns_price_EW = pd.Series.to_frame(df.iloc[:,1]/df.iloc[:,1].shift(1).replace(np.nan, 0))
    
    df = df.merge(returns_price_CW, on='date')
    df = df.merge(returns_price_EW, on='date')
    
    portfolio_CW = pd.Series.to_frame(df.iloc[1:,2].cumprod()*100)
    portfolio_EW = pd.Series.to_frame(df.iloc[1:,3].cumprod()*100)
    
    df = df.merge(portfolio_CW, on='date')
    df = df.merge(portfolio_EW, on='date')
    
    df.columns = ['cw_index', 'ew_index', 'cw_returns', 'ew_returns', 'cw_portfolio', 'ew_portfolio']
    if len(value) > 0:
        fig = go.Figure()
        for val in value:
            df = df[value]
            fig.update_layout(font_color="White",
                margin=dict(l=50, r=20, t=20, b=20),
                paper_bgcolor="rgb(0,0,0,0)", plot_bgcolor="rgb(0,0,0,0)", colorway=['#0AF047', '#0AEEF0'], xaxis=dict(showgrid=False),
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

