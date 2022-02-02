import requests
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime, timedelta
import time
import json
import os
from trending import get_trending

app = Flask(__name__)

@app.route('/')

if __name__ == "__main__":
     app.debug = False
     port = int(os.environ.get('PORT', 33507))
     waitress.serve(app, port=port)


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import json
import plotly.express as px

import urllib.request, json 
with urllib.request.urlopen('https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/eng/lad.json') as url:
    data = json.loads(url.read().decode())
    print(data)
data['features'][0]['geometry']

df = pd.read_csv('dft-road-casualty-statistics-accident.csv')

df1 = df[["accident_year","longitude","latitude","road_type","speed_limit","urban_or_rural_area","accident_severity"]].copy()
df1 = df1[df1["accident_year"] >= 2000]

df2 = df.groupby(["local_authority_district","accident_year","local_authority_ons_district"]).size().to_frame(name='no. of accidents').reset_index()
df2 = df2[df2["accident_year"] >= 2000]

#starting the app
app = dash.Dash(__name__)
server = app.server
# main app layout
app.layout = html.Div([
    #main title
    html.Div([
        html.H1('Road safety in the UK', id='title_text')
    ], id='title'),
    #start of the first container
    html.Div([
        #instruction text
        html.P('select a single year.', id='slider_text1'), 

        dcc.RadioItems(
            options=[
                {'label': '2000', 'value': 2000},
                {'label': '2001', 'value': 2001},
                {'label': '2002', 'value': 2002},
                {'label': '2003', 'value': 2003},
                {'label': '2004', 'value': 2004},
                {'label': '2005', 'value': 2005},
                {'label': '2006', 'value': 2006},
                {'label': '2007', 'value': 2007},
                {'label': '2008', 'value': 2008},
                {'label': '2009', 'value': 2009},
                {'label': '2010', 'value': 2010},
                {'label': '2011', 'value': 2011},
                {'label': '2012', 'value': 2012},
                {'label': '2013', 'value': 2013},
                {'label': '2014', 'value': 2014},
                {'label': '2015', 'value': 2015},
                {'label': '2016', 'value': 2016},
                {'label': '2017', 'value': 2017},
                {'label': '2018', 'value': 2018},
                {'label': '2019', 'value': 2019},
                {'label': '2020', 'value': 2020}   
            ],
            value=2020,#default year selected
            labelStyle={'display': 'inline-block',
                        'margin-right': '30px',
                        'margin-left': '10px',
                        'margin-bottom': '20px'},
            id='Select_Radio1'),
        dcc.Graph(id='map1')# the first map
    ],id='container1'),
    #end of the first container
    #
    #start of the second container
    html.Div([
        #instruction text
        html.P('select a single year.', id='slider_text2'), 
        #years selector
        dcc.RadioItems(
            options=[
                {'label': '2000', 'value': 2000},
                {'label': '2001', 'value': 2001},
                {'label': '2002', 'value': 2002},
                {'label': '2003', 'value': 2003},
                {'label': '2004', 'value': 2004},
                {'label': '2005', 'value': 2005},
                {'label': '2006', 'value': 2006},
                {'label': '2007', 'value': 2007},
                {'label': '2008', 'value': 2008},
                {'label': '2009', 'value': 2009},
                {'label': '2010', 'value': 2010},
                {'label': '2011', 'value': 2011},
                {'label': '2012', 'value': 2012},
                {'label': '2013', 'value': 2013},
                {'label': '2014', 'value': 2014},
                {'label': '2015', 'value': 2015},
                {'label': '2016', 'value': 2016},
                {'label': '2017', 'value': 2017},
                {'label': '2018', 'value': 2018},
                {'label': '2019', 'value': 2019},
                {'label': '2020', 'value': 2020}   
            ],
            value=2020,#default year selected
            labelStyle={'display': 'inline-block',
                        'margin-right': '30px',
                        'margin-left': '10px',
                        'margin-bottom': '20px'},
            id='Select_Radio2'),
        dcc.Graph(id='map2')# the second map
    ], id='container2')
    #end of the second container
    
], id='layout')

#first map callback
@app.callback(
    Output('map1','figure'), # the output (the first map)
    [Input('Select_Radio1','value')] # the input from the years selector
)

def update_graph(year_chosen):
    #modify the dataframe to display data corresponding the year selected
    dff=df2[df2['year'] == year_chosen]
    #making the map
    fig = px.density_mapbox(dff, lat='latitude',
                            lon='longitude',
                            z='control', radius=3.5,
                            opacity=0.9,
                            center=dict(lat=54.909865, lon=-1.918092),
                            zoom=5,height=700,
                            mapbox_style="dark",
                            template='plotly_dark',
                            color_continuous_scale='jet',
                            custom_data=['road type', 'speed_limit', 'urban or rural', 'accident severity'])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox_accesstoken=token, coloraxis=dict(showscale=False))
    #data that shows on hover
    fig.update_traces(
            hovertemplate="<br>".join([
                "Accident severity:  <b>%{customdata[3]}</b>",
                "Road type:  <b>%{customdata[0]}</b>",
                "Speed limit:  <b>%{customdata[1]}</b>",
                "Area type:  <b>%{customdata[2]}</b>"
            ]),
       )


    return fig

#second map callback
@app.callback(
    Output('map2','figure'),#output (the second map)
    [Input('Select_Radio2','value')] # input from the years selector
)

def update_graph(year_chosen):
    #modify the dataframe to display data corresponding to the year selected
    dff=df1[df1['accident_year']== year_chosen]
    dff['no. of accidents2'] = np.log(dff['no. of accidents'])
    
    vals=[1,2,3, 4, 5, 6, 7,8] #color scale values
    #making the second map
    fig = px.choropleth_mapbox(dff, geojson=districts,
                               locations='id',
                               featureidkey='properties.id',
                               color='no. of accidents2',
                               color_continuous_scale="jet",
                               mapbox_style="dark",
                               zoom=5,
                               center = {"lat": 54.909865, "lon": -1.918092},
                               height=700,
                               opacity=0.3,
                               labels={'no. of accidents2':'Frequency'},
                               custom_data=['district', 'no. of accidents'],
                               template='plotly_dark'
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox_accesstoken=token)
    fig.update_coloraxes(colorbar=dict(tickvals=vals, ticktext=np.round(np.exp(vals)), y=0.48))
    fig.update_traces(
        #data that shows on hover
            hovertemplate="<br>".join([
                "Local authority district:  <b>%{customdata[0]}</b>",
                "Accident frequency:  <b>%{customdata[1]}</b>",
            ]),
        )


    return fig
    
#running the app
if __name__ == "__main__":
    app.run_server(debug=True)
