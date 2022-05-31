import pandas as pd
import plotly.express as px 
import dash

# For interactive components like graphs, dropdowns, or date ranges.
from dash import dcc
# For HTML tags

#from dash.dependencies import Input, Output

import pandas as pd

# For graphics
import plotly.express as px 
import plotly.graph_objs as go

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

import plotly.express as px

#initialize the dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# # Import data and cleaning

#import data
df = pd.read_csv("Data/houses_venice_2.csv")
#remove bad columns
df = df.drop(columns=["Unnamed: 0"])
#drop nan value
df = df.dropna()
df = df.reset_index(drop=True)

#Clean price data
df["Price"] = df["Price"].str.replace('.','')
df["Price"] = df["Price"].str.replace('€','')
df["Price"] = df["Price"].str.split(' ', expand=True)[1].astype("float")
#clean size data
df["Size"] = df["Size"].str.replace('m²','').astype("float")
#clean floor data
df["Floor"] = df["Floor"].str.split(' ',expand=True)[0]
#clean room data
df["Room"] = df["Room"].str.replace('+','').astype("float")
#Clean flor data
df["Floor"] = df["Floor"].str.split(' ',expand=True)[0]
df["Floor"] = df["Floor"].str.replace('R',"0")
df["Floor"] = df["Floor"].str.replace('A',"0")
df["Floor"] = df["Floor"].str.replace('S',"-1")
df["Floor"] = df["Floor"].str.replace('T',"0").astype("float")
#reset index
df = df.reset_index(drop=True)
#calculate new variables
df["Price/Size"] = df["Price"]/df["Size"]
df["Price/Room"] = df["Price"]/df["Room"]
df["Price/Floor"] = df["Price"]/df["Room"]
#calculate mean variables by zone
df_zone = df.groupby("Zone").mean().reset_index()
#count number of houses
df_zone["Number_of_house"] = df.groupby("Zone").count().reset_index()["Name"]
#initialize zone variable for dropdown
zones = df["Zone"].unique()
df_zone = df_zone.reset_index()
#initialize heatmap
heatmap = px.imshow(df_zone.corr(),text_auto=True)
#initialize scatter plot
scatter_price_size = px.scatter(df, x="Price", y="Size",color="Zone",log_x=True, size_max=60, trendline="ols")
#initialize map
venice_map = open("price_size.html").read()
#initialize barchart
barchart = px.bar(df_zone.sort_values("Price",ascending=False), x="Zone", y="Price")


# # Dashboard
#CSS
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

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

#button and dropdwon
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
    ])

#sidebar with controls
sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

#first row --> text
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


#second row -->tables
content_second_row = dbc.Row(
    [
                html.Div(id='statistic_table_zone',className="md-6 col-6"),
                dbc.Table.from_dataframe(df_zone[["Zone","Price","Size"]], id="size_price_table_zone", striped=True, bordered=True, hover=True,responsive="md-6 col-6"),
    ], id="table_row"
)
#third row --> scatter plot and map
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
#fourth row --> heatmap and barchart
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
#group all the rows
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
#set layout 
app.layout = html.Div([sidebar,content])

#first callback for dropdwon values
@app.callback(
    # the dependencies refer to elements from the layout using id
    dash.dependencies.Output('price_vs_zone', 'figure'),
    dash.dependencies.Output('heatmap', 'figure'),
    dash.dependencies.Output('statistic_table_zone', 'children'),

    
    
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
#second call back for radio buttons
@app.callback(
    dash.dependencies.Output('price_zone_map', 'srcDoc'),
    dash.dependencies.Output('price_zone_bar', 'figure'),
   [
    dash.dependencies.Input('radio_items', 'value')]
    )
#upgrande map and barchart
def update_graph_2( radio):
    df_filterd = df_zone.sort_values("Price",ascending=False)
    venice_map = open("price_size.html").read()
    barchart = px.bar(df_filterd, x="Zone", y="Price")
    df_price_size = pd.DataFrame()
    if (radio=="price/size"):
        df_price_size = df_zone.sort_values("Price/Size",ascending=False)
        venice_map = open("price_size_map.html").read()
        barchart =  px.bar(df_price_size, x="Zone", y="Price/Size")
    return venice_map, barchart
    
if __name__ == '__main__':
    app.run_server(debug=True)



