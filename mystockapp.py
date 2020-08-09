import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output


app = dash.Dash()
server = app.server

all_data=dict()
all_data['twtr'] = pd.read_csv("data/TWTR.csv")
all_data['ino'] = pd.read_csv("data/INO.csv")
all_data['gps'] = pd.read_csv("data/GPS.csv")
all_data['tsla'] = pd.read_csv("data/TSLA.csv")
all_data['azn'] = pd.read_csv("data/AZN.csv")
all_data['tlry'] = pd.read_csv("data/TLRY.csv")
all_data['jmia'] = pd.read_csv("data/JMIA.csv")
all_data['nvax'] = pd.read_csv("data/NVAX.csv")
all_data['cgc'] = pd.read_csv("data/CGC.csv")

app.layout = html.Div(children=[
    # Main title of dashboard
    html.H1(children="Twitter Stock",style={"textAlign": "center"}),
    # Create Dashboard Tab Layout
    dcc.Tab(id="Stock Prices", children=[
        html.Div([
            html.H1("Stock Highs vs Lows",
                   style={'textAlign':'center'}),
            #Add dropdown menu
            dcc.Dropdown(id='my-dropdown', options=[{'label':'Twitter','value':'TWTR'},
                                                   {'label':'Inovio','value':'INO'},
                                                    {'label':'Gap','value':'GPS'},
                                                    {'label':'AstraZeneca','value':'AZN'},
                                                    {'label':'Tilray','value':'TLRY'},
                                                    {'label':'Jumia Technologies','value':'JMIA'},
                                                    {'label':'Novavax','value':'NVAX'},
                                                    {'label':'Canopy Growth','value':'CGC'}],
                         multi=True, value=['TWTR'],
                         style={"display":"block","margin-left":"auto","margin-right":"auto","width":"60%"}),
            dcc.Graph(id='highlow',figure={}),
            html.H1('Market Volume', style={'textAlign':'center'}),
            #Adding the second dropdown menu and graph
            dcc.Dropdown(id='my-dropdown2',
                        options=[{'label':'Twitter','value':'TWTR'},
                                {'label':'Inovio','value':'INO'},
                                {'label':'Gap','value':'GPS'},
                                {'label':'AstraZeneca','value':'AZN'},
                                {'label':'Tilray','value':'TLRY'},
                                {'label':'Jumia Technologies','value':'JMIA'},
                                {'label':'Novavax','value':'NVAX'},
                                {'label':'Canopy Growth','value':'CGC'}],
                         multi=True, value=['TWTR'],
                         style={'display':'block','margin-left':'auto',
                               'margin-right':'auto','width':'60%'}),
            dcc.Graph(id='volume')
        ], className='container'),
        ])
    ])


@app.callback(Output("highlow","figure"),
             [Input('my-dropdown','value')])
def update_graph(selected_dropdown):
    dropdown={"TWTR":"Twitter","INO":"Inovio","GPS":"Gap","AZN":"AstraZeneca","TLRY":"Tilray","JMIA":"Jumia Technologies","NVAX":"Novavax","CGC":"Canopy Growth"}
    trace1 = []
    trace2 = []
    for stock in selected_dropdown:
        trace1.append(
            go.Scatter(x=all_data[stock.lower()]['Date'],y=all_data[stock.lower()]['High'],
                       mode='lines',opacity=0.7,
                       name=f'High {stock}', textposition='bottom center'))
        trace2.append(
            go.Scatter(x=all_data[stock.lower()]['Date'],y=all_data[stock.lower()]['Low'],
                      mode='lines',opacity=0.6,
                      name=f'Low {stock}',textposition='bottom center'))
    traces = [trace1, trace2]
    data1 = [val for sublist in traces for val in sublist]
    figure = {'data':data1,
            'layout':go.Layout(colorway=['#5E0DAC', '#FF4F00','#375CB1',
                                        '#FF7400', '#FFF400', '#FF0056'],
                                height=600,
                                title=f"High and Low Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
                                xaxis={"title":"Date",
                                        'rangeselector': {'buttons': list([{'count': 1, 'label':'1M',
                                                                             'step':'month',
                                                                             'stepmode':'backward'},
                                                                            {'count': 6, 'label': '6M',
                                                                            'step':'month',
                                                                            'stepmode':'backward'},
                                                                            {'step': 'all'}])},
                                           'rangeslider':{'visible':True}, 'type':'date'},
                                yaxis={"title":"Price (USD)"})}

    return figure

@app.callback(Output('volume','figure'),
             [Input('my-dropdown2','value')])
def update_graph(selected_dropdown_value):
    dropdown = {"TWTR":"Twitter","INO":"Inovio","GPS":"Gap","AZN":"AstraZeneca","TLRY":"Tilray","JMIA":"Jumia Technologies","NVAX":"Novavax","CGC":"Canopy Growth"}
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(
        go.Scatter(x=all_data[stock.lower()]['Date'],
                  y=all_data[stock.lower()]['Volume'],
                  mode='lines', opacity=0.7,
                  name=f'Volume {stock}', textposition='bottom center'))
    traces = [trace1]
    data1 = [val for sublist in traces for val in sublist]
    figure = {'data': data1,
              'layout': go.Layout(colorway=['#5E0DAC', '#FF4F00', '#375CB1', 
                                            '#FF7400', '#FFF400', '#FF0056'],
            height=600,
            title= f"Market Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M',
                                                       'step': 'month', 
                                                       'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},
             yaxis={"title":"Transactions Volume"})}
    return figure

if __name__=='__main__':
    app.run_server(debug=False)