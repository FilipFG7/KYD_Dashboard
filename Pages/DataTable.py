import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback, State
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__)

df = pd.read_csv(r'C:\Users\Filip\Desktop\Codes\KYD-Dashboard\ifood_df.csv')
df = df[['Income','MntWines','MntFruits','MntMeat','MntFish','MntSweet','MntGold','MntTotal']]
df.insert(0, 'Cust', range(1, 1 + len(df))) 

def layout():   
    return dbc.Container([
        dcc.Markdown('# Data table with income slider', style={'textAlign':'center'}),        
        dash_table.DataTable(
            columns=[
                {'name': 'Cust', 'id': 'Cust', 'type': 'numeric'},
                {'name': 'Income', 'id': 'Income', 'type': 'numeric'},
                {'name': 'MntWines', 'id': 'MntWines', 'type': 'numeric'},
                {'name': 'MntFruits', 'id': 'MntFruits', 'type': 'numeric'},
                {'name': 'MntMeat', 'id': 'MntMeat', 'type': 'numeric'},
                {'name': 'MntFish', 'id': 'MntFish', 'type': 'numeric'},
                {'name': 'MntSweet', 'id': 'MntSweet', 'type': 'numeric'},
                {'name': 'MntGold', 'id': 'MntGold', 'type': 'numeric'},
                {'name': 'MntTotal', 'id': 'MntTotal', 'type': 'numeric'}
            ],
            data=df.to_dict('records'),            
            id='table',
            editable=True,
            page_size= 10,           
        ),        
        dbc.Row([
            dbc.Col([
                dcc.RangeSlider(0, 120000, 5000, value=[50000,60000], id='income_slider')
            ], width=11)    
        ])
    ])

@callback(
    Output('table', 'data'),
    Input('income_slider', 'value'), 
)
def update_dropdown_options(income_v1):
    dff = df.copy()

    dff=dff[(df['Income']>=income_v1[0])&(df['Income']<=income_v1[1])]

    return dff.to_dict('records')
