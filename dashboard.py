import dash  # use Dash version 1.16.0 or higher for this app to work
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_table
from dash_table.Format import Format, Scheme


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
        options=[{'label': '  Cap Weighted', 'value': 'cap_weighted_index'},
                 {'label': '  Equal Weighted', 'value': 'ponderated_index'},
                 {'label': '  Minimum Variance', 'value': 'MV'},
                 {'label': '  High Volatility', 'value': 'HV'},
                 {'label': '  Low Volatility', 'value': 'LV'},
                 {'label': '  Risk Parity', 'value': 'RP'},
                 {'label': '  Low Beta', 'value': 'LB'},
                 {'label': '  High Beta', 'value': 'HB'},
                 ],
        value=['cap_weighted_index', 'ponderated_index'],
        labelStyle={'display': 'block'}
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
                {'label': '100 Crypto Model', 'value': 'metrics2.csv'},
                {'label': 'Third Crypto Model', 'value': 'metrics3.csv'}
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
    df = pd.read_csv(f'data/strats/all_price_20_1e6.csv')
    df.set_index('datetime', inplace=True)
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


@app.callback(
    Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data'),
    Input(component_id='dropdown', component_property='value'),
)

def update_output(val):
    df3 = pd.read_csv(r'data/processed/df_metrics_20_1e6.cs')
    df4 = pd.read_csv(r'data/processed/df_metrics_100_1e6.cs')
    df5 = pd.read_csv(r'data/processed/df_metrics_20_1e6.cs')
    if val == "metrics1.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=2, scheme=Scheme.fixed), "type":'numeric'} for i in df3.columns]
        data=df3.to_dict('records')
        return columns, data
    elif val == "metrics2.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=2, scheme=Scheme.fixed), "type":'numeric'} for i in df4.columns]
        data=df4.to_dict('records')
        return columns, data
    elif val == "metrics3.csv":
        columns = [{"name": i, "id": i, "format": Format(precision=2, scheme=Scheme.fixed), "type":'numeric'} for i in df5.columns]
        data=df5.to_dict('records')
        return columns, data

if __name__ == '__main__':
    app.run_server(debug=True)
