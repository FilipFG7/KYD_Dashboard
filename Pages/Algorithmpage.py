#libraries for building the webapp page
import pandas as pd
import numpy as np
from logging import PlaceHolder
from pydoc import classname
import dash
from dash import Dash, html, dcc, Input, Output, callback, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px 
#import pages_plugin
import dash_labs as dl
import dash_auth
from numpy import size 
from ctypes import alignment
# libraries for machine learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import  accuracy_score
import wrapt
#libraries to save the excel file uploaded on webapp
import base64
import datetime
import io
import json

# inserting this page into the webapp built in different code
dash.register_page(__name__, path="/")

# text displayed on the page
upload_info= '''
#### **Please upload the excel file with customer's data to predict the income range.**
'''

# page layout
def layout():
    return dbc.Container(
        [
            dbc.Row([
                dbc.Col(html.Div(children=[
                    # displays text on the page
                    html.Hr(),                    
                    dcc.Markdown(children=upload_info, className='text-center'),                    
                    html.Hr()                   
                ],className="column"
                ),
                    width={'size':12, 'order':1}),                    
            ]),
            dbc.Row([    
                dbc.Col(html.Div(children=[
                    # creates a box where the user can upload the file
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([

                            'Drag and drop or select a file',
                            #html.A('select a File')
                    ]), style={                        
                        'height': '70px',
                        'lineHeight': '60px',
                        'borderWidth': '3px',
                        'borderStyle': 'dashed',
                        'borderRadius': '8px',
                        'textAlign': 'center',
                        'backgroundColor':'#262626',
                        'color':'#F2F2F2',
                        'font-size':'25px',
                        'width': '6'
                    },
                    multiple=True,                    
                    ),               
                ]),
                    width={'size':5}),
                dbc.Col(html.Div(id='output-file'))
            ]),
            
            dbc.Row([
                #dbc.Col(html.Div(id='results')                   
                #),                
                dbc.Col(html.Div(children=[
                    html.Br(),
                    # button that starts the machine learning function
                    html.Button('Submit', id='submit-value', n_clicks=0, style={'font-size':'29px', 
                    'width':'160px', 'height':'40px','background-color':'#F2F2F2', 'color':'#262626','borderRadius': '7px'}),
                    html.Br()
                ]),
                    #align='end',
                    width={'size':3, 'order':2}
                ),
                
            ]),
            dbc.Row([
                dbc.Col(html.Div(id='results'), width={'size':8, "offset": 2}                   
                ),

            ]),
                  
        ],fluid=True
    )

# function that has the algorithm to predict the income of customer
# based on the amount of products
def machine_learning():
    # Forming dataframes for the machine learning and predicting for a random user
    df=pd.read_csv(r'C:\Users\Filip\Desktop\Codes\KYD-Dashboard\ifood_df.csv')
    df1=pd.read_excel(r'C:\Users\Filip\Desktop\Codes\KYD-Dashboard\Customer.xlsx')

    # Cleaning up the data
    columns=['Kidhome','Teenhome','Recency','NumDealsPurchases','NumWebPurchases','NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5','AcceptedCmp1','AcceptedCmp2','Complain','Z_CostContact','Z_Revenue','Response','Age','Customer_Days','marital_Divorced','marital_Married','marital_Single','marital_Together','marital_Widow','education_2n Cycle','education_Basic','education_Graduation','education_Master','education_PhD','AcceptedCmpOverall']
    df = df.drop(columns, axis=1)
    df["Income"]=np.where((df["Income"] <10000) & (df['Income'] > 0), 0, df['Income'])
    df["Income"]=np.where((df["Income"] <20000) & (df['Income'] > 10000), 1, df['Income'])
    df["Income"]=np.where((df["Income"] <30000) & (df['Income'] > 20000), 2, df['Income'])
    df["Income"]=np.where((df["Income"] <40000) & (df['Income'] > 30000), 3, df['Income'])
    df["Income"]=np.where((df["Income"] <50000) & (df['Income'] > 40000), 4, df['Income'])
    df["Income"]=np.where((df["Income"] <60000) & (df['Income'] > 50000), 5, df['Income'])
    df["Income"]=np.where((df["Income"] <70000) & (df['Income'] > 60000), 6, df['Income'])
    df["Income"]=np.where((df["Income"] <80000) & (df['Income'] > 70000), 7, df['Income'])
    df["Income"]=np.where((df["Income"] <90000) & (df['Income'] > 80000), 8, df['Income'])
    df["Income"]=np.where((df["Income"] <1000000) & (df['Income'] > 90000), 9, df['Income'])
    df["Income"]=np.where((df["Income"] >1000000), 10, df['Income'])

    # Modifying dataframes for the axis for ML
    x = pd.get_dummies(df.drop(['Income'], axis=1))
    y = df['Income']

    #Splitting data
    xtrain, xtest, ytrain, ytest = train_test_split(x, y,test_size=0.3, random_state = 42)

    #Random Forest Classifier model
    model = RandomForestClassifier(n_estimators=600, min_samples_split=5, min_samples_leaf= 1, max_depth= 80, bootstrap= True)
    model.fit(xtrain, ytrain)

    #Accurcy metrics
    score = model.score(xtest, ytest)
    #print(score)

    # Adding and changing the new value for Income
    # to the second dataframe and creating an excel file
    k=model.predict(df1)
    df1['Income']=list(k)
    df1['Income']=df1['Income'].replace(0,'Less than 10k')
    df1['Income']=df1['Income'].replace(1,'10k-20k')
    df1['Income']=df1['Income'].replace(2, '20k-30k')
    df1['Income']=df1['Income'].replace(3, '30k-40k')
    df1['Income']=df1['Income'].replace(4, '40k-50k')
    df1['Income']=df1['Income'].replace(5, '50k-60k')
    df1['Income']=df1['Income'].replace(6, '60k-70k')
    df1['Income']=df1['Income'].replace(7, '70k-80k')
    df1['Income']=df1['Income'].replace(8, '80k-90k')
    df1['Income']=df1['Income'].replace(9,'90k-100k')
    df1['Income']=df1['Income'].replace(10,'More than 100k')
    df1.to_excel("./Predict.xlsx",index=False)

    #Adjust the excel file
    columns1 =['MntWines','MntFruits','MntMeat','MntFish','MntSweet','MntGold','MntRegularProds']
    df1.insert(0, 'Customer', range(1, 1 + len(df1)))
    df1=df1.drop(columns1, axis=1)
   
    # create a dash table
    table = dbc.Table.from_dataframe(df1, striped=True, bordered=True)
    
    return html.Div([
        html.Br(),
        html.H4('This is the prediction of the customers income and the amount of total items bought',className='text-center'),
        html.Hr(),
        table
    ])
            
#function that saves the data that the user uploaded into the pc 
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df2 = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df2 = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        #html.Br(),        
        html.H4(
            children='Your data has been saved. To see the expected income of the customer, please press the button.',
            style={'padding-top':'8px','borderRadius': '9px','width':'6','textSize':'100%','textAlign': 'center','background-color':'#262626', 'height':'70px', 'color':'#F2F2F2'}
            ),                
        dcc.Store(id="stored-data", data=df2.to_excel('Customer.xlsx',index=False))
    ])

# first callback that takes the input from the user in a form of excel file and gives output
@callback(
    Output('output-file','children'),
    [Input('upload-data', 'contents'), Input('upload-data','filename')],
)

# funtion that runs the parse_contents() funtion if the file inserted has some values in it 
def save_data(contents,filename):
    if contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(contents, filename)]
        return children   
# second callback which takes the input from the user in a form of a button click and gives output   
@callback(
    Output('results','children'),
    [Input('submit-value','n_clicks')],
)
# function that starts the machine learning function after the button was pressed
def present_data(button):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit-value' in  changed_id:
        return machine_learning()
    else:
        print()
