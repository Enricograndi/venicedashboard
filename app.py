#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.graph_objs as go
import networkx as nx
import folium
import geopandas as gpd
from dash import  dash_table
import dash

# For interactive components like graphs, dropdowns, or date ranges.
import dash_core_components as dcc 

# For HTML tags
import dash_html_components as html

from dash.dependencies import Input, Output

import pandas as pd

# For graphics
import plotly.express as px 
import plotly.graph_objs as go

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# # Import data and cleaning

# In[ ]:


#import data
df = pd.read_csv("Data/houses_venice_2.csv")
#remove bad columns
df = df.drop(columns=["Unnamed: 0"])
#drop nan value
df = df.dropna()
df = df.reset_index(drop=True)


# In[ ]:


df["Price"] = df["Price"].str.replace('.','')
df["Price"] = df["Price"].str.replace('€','')
df["Price"] = df["Price"].str.split(' ', expand=True)[1].astype("float")


# In[ ]:


df["Size"] = df["Size"].str.replace('m²','').astype("float")
df["Floor"] = df["Floor"].str.split(' ',expand=True)[0]
df["Room"] = df["Room"].str.replace('+','').astype("float")


# In[ ]:


df["Floor"] = df["Floor"].str.split(' ',expand=True)[0]
df["Floor"] = df["Floor"].str.replace('R',"0")
df["Floor"] = df["Floor"].str.replace('A',"0")
df["Floor"] = df["Floor"].str.replace('S',"-1")
df["Floor"] = df["Floor"].str.replace('T',"0").astype("float")


# In[ ]:


df = df.reset_index(drop=True)
df["Price/Size"] = df["Price"]/df["Size"]
df["Price/Room"] = df["Price"]/df["Room"]
df["Price/Floor"] = df["Price"]/df["Room"]


# In[ ]:


df_zone = df.groupby("Zone").mean().reset_index()
df_zone["Number_of_house"] = df.groupby("Zone").count().reset_index()["Name"]

df_zone = df_zone.set_index("Zone")
df_zone = df_zone.reset_index()

zones = df["Zone"].unique()

heatmap = px.imshow(df_zone.corr(),text_auto=True)
heatmap

scatter_price_size = px.scatter(df, x="Price", y="Size",color="Zone",
                 log_x=True, size_max=60, trendline="ols")



# # Dashboard

# In[ ]:


venice_map = open("price_size.html").read()
barchart = px.bar(df_zone.sort_values("Price",ascending=False),
                      x="Zone", y="Price")


# In[ ]:


controls = dbc.Row(
    [
        html.P('Dropdown', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='zone',
            options=[{'label': i, 'value': i} for i in zones]+ [{'label': 'Select all', 'value': 'all_values'}],
            value=['all_values'],  # default value
            multi=True
        ),
        html.P('Choose map and Barchart Variable', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.RadioItems(
            id='radio_items',
            options=[{
                'label': 'Price',
                'value': 'price'
            },
                {
                    'label': 'Price/Size',
                    'value': 'price/size'
                }
            ],
            value='price',
            style={
                'margin': 'auto'
            }
        )])
    ]
)

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}


sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)


# In[ ]:


CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=6
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4('Card Title 2', className='card-title', style=CARD_TEXT_STYLE),
                        html.P('Sample text.', style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=6
    ),
    
    
])


# In[ ]:




# In[ ]:


content_second_row = dbc.Row(
    [
                html.Div(id='statistic_table_zone',className="md-6 col-6"),
                dbc.Table.from_dataframe(df_zone[["Zone","Price","Size"]], id="size_price_table_zone", striped=True, bordered=True, hover=True,responsive="md-6 col-6"),

                


    ], id="table_row"
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='price_vs_zone',
        figure=scatter_price_size), md=6
        ),
        dbc.Col(
            html.Iframe(id='price_zone_map',
            srcDoc=venice_map,width="100%",height="600"), md=6
        )
    ], id="grapg_row_1"
)

content_fourth_row = dbc.Row(
    [
        
        dbc.Col(
            dcc.Graph(id="heatmap",figure=heatmap), md=6
        ),
        dbc.Col(
            dcc.Graph(id='price_zone_bar',
            figure=barchart), md=6
        )
    ], id="grapg_row_2"
)


# In[ ]:


CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

content = html.Div(
    [
        html.H2('Analytics Dashboard Template', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_second_row,
        content_third_row,
        content_fourth_row
    ],
    style=CONTENT_STYLE
)


# In[ ]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([sidebar,content])


# In[ ]:


@app.callback(
    # the dependencies refer to elements from the layout using id
    dash.dependencies.Output('price_vs_zone', 'figure'),
    dash.dependencies.Output('heatmap', 'figure'),

    
    
        # input 2:
   [dash.dependencies.Input('zone', 'value')]
    
    )

# def update_graph(input 1,input 2)

def update_graph_1(zona):
    filtered_df = df
    scatter_price_size = px.scatter(df, x="Price", y="Size",color="Zone",
                 log_x=True, size_max=60, trendline="ols")
    heatmap = px.imshow(df.corr(),text_auto=True)
    table = dbc.Table.from_dataframe(df.describe()[["Price","Size"]].reset_index(), striped=True, bordered=True, hover=True)
    
    if (zona!="all_values"):
        new_filterd_df = pd.DataFrame()
        for z in zona: 
            new_filterd_df = pd.concat([new_filterd_df,df[df["Zone"]==z]])
            print(zona)
            
        scatter_price_size = px.scatter(new_filterd_df, x="Price", y="Size",color="Zone",
                 log_x=True, size_max=60, trendline="ols")
        heatmap = px.imshow(new_filterd_df.corr(),text_auto=True)
        table = dbc.Table.from_dataframe(new_filterd_df.describe()[["Price","Size"]].reset_index(), striped=True, bordered=True, hover=True)

        
    if (zona[0]=="all_values"):
        scatter_price_size = px.scatter(filtered_df, x="Price", y="Size",color="Zone",
                 log_x=True, size_max=60, trendline="ols")
        heatmap = px.imshow(filtered_df.corr(),text_auto=True)
        table = dbc.Table.from_dataframe(filtered_df.describe()[["Price","Size"]].reset_index(), striped=True, bordered=True, hover=True)

    return scatter_price_size, heatmap, table


# In[ ]:


@app.callback(
    # the dependencies refer to elements from the layout using id
   
    
    dash.dependencies.Output('price_zone_map', 'srcDoc'),
    dash.dependencies.Output('price_zone_bar', 'figure'),
    
        # input 2:
   [
    dash.dependencies.Input('radio_items', 'value')]
    
    )

def update_graph_2( radio):
    df_filterd = df_zone.sort_values("Price",ascending=False)
    venice_map = open("price_size.html").read()
    barchart = px.bar(df_filterd, x="Zone", y="Price")
    print(radio)
    df_price_size = pd.DataFrame()
    if (radio=="price/size"):
        df_price_size = df_zone.sort_values("Price/Size",ascending=False)
        venice_map = open("price_size_map.html").read()
        barchart =  px.bar(df_price_size, x="Zone", y="Price/Size")
    
        
    return venice_map, barchart


# In[ ]:


app.run_server()


# In[ ]:




