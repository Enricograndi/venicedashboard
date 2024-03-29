import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px 
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# # Import data and cleaning

#import data
df = pd.read_csv("Data/df_heroku.csv")
df_zone = pd.read_csv("Data/df_zone_heroku.csv")
zones = df["Zone"].unique()

#initialize heatmap
global heatmap 
heatmap = px.imshow(df_zone.corr(),text_auto=True)
#initialize scatter plot
global scatter_price_size
scatter_price_size = px.scatter(df, x="Price", y="Size",color="Zone",log_x=True, size_max=60, trendline="ols")
#initialize map
global venice_map
venice_map = open("asset/price_size.html").read()
#initialize barchart
global barchart
barchart = px.bar(df_zone.sort_values("Price",ascending=False), x="Zone", y="Price",  color="Zone")


# # Dashboard
#CSS
TEXT_STYLE = {
    'textAlign': 'left',
    'color': 'black'
}
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'backgroundColor': '#f8f9fa'
}

CARD_TEXT_STYLE = {
    'textAlign': 'left',
    'color': 'black'
}
CONTENT_STYLE = {
    'marginLeft': '25%',
    'marginRight': '5%',
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
content_first_table = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
            dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['The project'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['''
                        The project aims at analyzing apartment prices in Venice and understand their main determinants by investigating Immobiliare.it, the main website used by Italian real estate agent.
                        Indeed, Venice is a maritime city built upon a group of small islands divided by canals and connected with bridges and a mainland area linked to the main island by rail and road bridges over the lagoon. The objective is to see whether this special and unique conformation impacts prices of apartments for sale as well as if it has an influence on prices’ determinants. 
                        More precisely, the questions we aim to answer are:'''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_1', children=['''
                        •	Is there a correlation between sale prices and the location?
                        '''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_2', children=['''
                         •	Is there a correlation between sale prices and the size?
                        '''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_3', children=['''
                        •	Is there a correlation between sale prices and the number of rooms?
                        '''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_4', children=['''
                        •	Is there a correlation between sale prices and the floor?
                        '''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_5', children=['''
                        •	What are the zones with more apartments for sale?
                        '''], style=CARD_TEXT_STYLE),
                        html.P(id='card_text_par_6', children=['''
                        We display our main results using tables and charts that jointly vary based on the chosen parameters. 
                        '''], style=CARD_TEXT_STYLE),
                     
                    ]
                ),
                
            ]
        ),
        md=12
    ),
    html.Br(),
    dbc.Col(
        dbc.Card(
            [dbc.CardBody([
                html.H4(id='card_title_2', children=['General statistical analysis of data'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2', children=['''
                        The table gives a first look at the data gathered and shows the number of houses and the mean, standard deviation, minimum and maximum, 25th percentile, 50th percentile and 75th percentile of both prices and size of the sample. 
                        '''], style=CARD_TEXT_STYLE)])
               
            ]

        ),
        md=12
    ),html.Br(),
    html.Div(id='statistic_table_zone',className="md-6 col-12"),
    
    
    
],className="gy-5")

#second row -->tables
content_second_table = dbc.Row([
    dbc.Col(
        dbc.Card(
            [
            dbc.CardBody(
                    [
                        html.H4(id='card_title_table2_1', children=['Mean price and size for Venice’s zones'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_table2_1', children=['''
                       The table shows the average price and size of apartments for sale in each Venetian zone. '''], style=CARD_TEXT_STYLE)
                     
                    ]
                ),
                
            ]
        ),
        md=12
    ),html.Br(),
    dbc.Table.from_dataframe(df_zone[["Zone","Price","Size"]], id="size_price_table_zone", striped=True, bordered=True, hover=True,responsive="md-6 col-12"),

    
    
    
],className="gy-5")


#third row --> scatter plot and map
content_first_graph = dbc.Row(
    [
        dbc.Col(
        dbc.Card(
            [
            dbc.CardBody(
                    [
                        html.H4(id='card_title_graph_1', children=['Correlation between price and size'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_graph_1', children=['''
                       The dynamic scatterplot analyzes the correlation between price (in €) and size (in m2).
                    It shows a positive relation between the two variables. 
 '''], style=CARD_TEXT_STYLE)
                     
                    ]
                ),
                
            ]
        ),
        md=12),
        dbc.Col(
            dcc.Graph(id='price_vs_zone',
        figure=scatter_price_size), md=12
        )
    ], id="grapg_row_1"
)
#fourth row --> heatmap and barchart
content_map = dbc.Row(
    [
        dbc.Col(
        dbc.Card(
            [
            dbc.CardBody(
                    [
                        html.H4(id='card_title_map', children=['Price and price per square meter based on zone'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_map_1', children=['''
                        The Venice map and the barchart below dynamically show either price or price per square meter according to the different zones. 
                      '''], style=CARD_TEXT_STYLE)
                      ,
                        html.P(id='card_text_map_2', children=['''
                        In the map, as the color gets darker, the price or price/size increases and the houses are relatively more expensive.
                      '''], style=CARD_TEXT_STYLE)
                      ,
                        html.P(id='card_text_map_3', children=['''
                        The cheapest zone where to buy an apartment is represented by the mainland, while XX is the most expensive in terms of absolute prices and XX and YY have the highest prices per square meter. 
                      '''], style=CARD_TEXT_STYLE)
                     
                    ]
                ),
                
            ]
        ),
        md=12),
        dbc.Col(
            html.Iframe(id='price_zone_map',
            srcDoc=venice_map,width="100%",height="600"), md=12, className="gy-5"
        ),
          dbc.Col(
            dcc.Graph(id='price_zone_bar',
            figure=barchart), md=12
        )
    ], id="content_map"
)


content_second_graph = dbc.Row(
    [
        dbc.Col(
        dbc.Card(
            [
            dbc.CardBody(
                    [
                        html.H4(id='card_title_graph_2', children=['Correlation between variables'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_graph_2', children=['''
                       The heatmap shows the correlation between all the variables.
                        The hotter the color, the stronger the correlation.
                     '''], style=CARD_TEXT_STYLE)
                     
                    ]
                ),
                
            ]
        ),
        md=12),
        dbc.Col(
            dcc.Graph(id="heatmap",figure=heatmap), md=12
        )
    ], id="grapg_row_2"
)

#group all the rows
content = html.Div(
    [
        html.H1('The distribution of prices of apartments for sale in Venice', style=TEXT_STYLE),
        html.P('by Bonamigo Luca, Farigliani Alessia, Terrana Lina', style=CARD_TEXT_STYLE),
        html.Hr(),
        content_first_table,
        content_second_table,
        content_first_graph,
        content_map,
        content_second_graph,
        html.Hr(),
        html.P('''Data and source: Data have been gathered on May 15, 2022 from the immobiliare.it website by using the beautiful soup and request methodologies and analyzed through pandas. 
                  Script on the github folder.''', style=CARD_TEXT_STYLE),
        html.P('''Venice coordinates are from: https://interactivegeomaps.com/venice-map-using-custom-source/''', style=CARD_TEXT_STYLE),
    ],
    style=CONTENT_STYLE
)
#initialize the dash
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
    #filtered_df = df
    #scatter_price_size = px.scatter(df, x="Price", y="Size",color="Zone", log_x=True, size_max=60, trendline="ols")
    #heatmap = px.imshow(df.corr(),text_auto=True)
    #for z in zona: 
    if ("all_values" in zona):
        table = dbc.Table.from_dataframe(df.describe()[["Price","Size"]].reset_index(), striped=True, bordered=True, hover=True)
        return scatter_price_size, heatmap, table
    
    new_filterd_df = df[df["Zone"].isin(zona)]
    scatter_price_size_filterd = px.scatter(new_filterd_df, x="Price", y="Size",color="Zone",
                 log_x=True, size_max=60, trendline="ols")
    heatmap_filtered = px.imshow(new_filterd_df.corr(),text_auto=True)
    table_filters = dbc.Table.from_dataframe(new_filterd_df.describe()[["Price","Size"]].reset_index(), striped=True, bordered=True, hover=True)
    return scatter_price_size_filterd, heatmap_filtered, table_filters
        

        

#second call back for radio buttons
@app.callback(
    dash.dependencies.Output('price_zone_map', 'srcDoc'),
    dash.dependencies.Output('price_zone_bar', 'figure'),
   [
    dash.dependencies.Input('radio_items', 'value')]
    )
#upgrande map and barchart
def update_graph_2( radio):
   #
    if (radio=="price/size"):
        venice_map_filterd = open("asset/price_size_map.html").read()
        barchart_filtered =  px.bar(df_zone.sort_values("Price/Size",ascending=False), x="Zone", y="Price/Size",  color="Zone")
        return venice_map_filterd, barchart_filtered
    else:
        return venice_map,barchart
#run the app
app.run_server(debug=True)