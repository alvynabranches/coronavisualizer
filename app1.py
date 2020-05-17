import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import base64
from datetime import  datetime, timedelta
from preprocessing import text_to_date

df = pd.read_csv('./data/covid_19_india.csv').drop(['Sno'], axis=1).dropna()
df['Date'] = df['Date'].apply(lambda x: text_to_date(x))
unique_states = list(df['State/UnionTerritory'].unique())
# features = df.columns
features = ['All', 'ConfirmedIndianNational', 'ConfirmedForeignNational', 'Cured', 'Deaths']

def print_time():
    return str('Login Time') + str(datetime.now())

app = dash.Dash()
server = app.server

app.layout = html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis',
                options=[{'label': i, 'value': i} for i in unique_states],
                value=unique_states[0]
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in features],
                value=features[0]
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='feature-graphic'),
    html.Div([
            html.Center([
                html.H4('Updated on 03/04/2020. From Kaggle Dataset.', style={'text-size': 30}),
                html.P('By Alvyn Abranches.'),
                html.Div(id='live-update-text'),
                dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
            ])
        ])
], style={'padding':10})

@app.callback(Output('feature-graphic', 'figure'), [Input('xaxis', 'value'), Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    if yaxis_name == 'All':
        limited_df = df[df['State/UnionTerritory'] == str(xaxis_name)]
        return {
            'data': [
                go.Scatter(
                    x=limited_df['Date'],
                    y=limited_df['ConfirmedIndianNational'],
                    mode='lines',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='Confirmed Indian National'
                ),
                go.Scatter(
                    x=limited_df['Date'],
                    y=limited_df['ConfirmedForeignNational'],
                    mode='lines',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='Confirmed Foreign National'
                ),
                go.Scatter(
                    x=limited_df['Date'],
                    y=limited_df['Cured'],
                    mode='lines',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='Cured'
                ),
                go.Scatter(
                    x=limited_df['Date'],
                    y=limited_df['Deaths'],
                    mode='lines',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line' : {'width': 0.5, 'color': 'white'}
                    },
                    name='Deaths'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': xaxis_name},
                yaxis={'title': 'All'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }
    else:
        limited_df = df[df['State/UnionTerritory'] == str(xaxis_name)]
        return {
            'data': [go.Scatter(
                x=limited_df['Date'],
                y=limited_df[yaxis_name],
                text=limited_df['State/UnionTerritory'],
                mode='lines',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )],
            'layout': go.Layout(
                xaxis={'title': xaxis_name},
                yaxis={'title': yaxis_name},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_date(n):
    return [
        html.P('Current Time ' + str(datetime.now() - timedelta(hours=5, minutes=30)) + ' IST'),
        html.P(str(datetime(year=2020, month=4, day=14, hour=23, minute=59, second=59, microsecond=99999) - datetime.now() - timedelta(hours=5, minutes=30)).split('.')[0] + ' Time Left To Finish Lockdown'),
        html.P(str(datetime(year=2020, month=4, day=30, hour=23, minute=59, second=59, microsecond=99999) - datetime.now() - timedelta(hours=5, minutes=30)).split('.')[0] + ' Time Left To Finish Lockdown, if Lockdown extends till 30th April'),
        html.P(str(datetime(year=2020, month=5, day=31, hour=23, minute=59, second=59, microsecond=99999) - datetime.now() - timedelta(hours=5, minutes=30)).split('.')[0] + ' Time Left To Finish Lockdown, if Lockdown extends till 31st May'),
        html.P(str(datetime(year=2020, month=6, day=30, hour=23, minute=59, second=59, microsecond=99999) - datetime.now() - timedelta(hours=5, minutes=30)).split('.')[0] + ' Time Left To Finish Lockdown, if Lockdown exts till 30th June')
    ]
if __name__ == '__main__':
    app.run_server()