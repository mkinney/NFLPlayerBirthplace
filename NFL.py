# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 14:58:43 2019

@author: ANDBER
"""

#LOAD LIBRARY
import requests
import pandas as pd
import numpy as np
import itertools
import plotly.graph_objects as go
from plotly.offline import plot






## Dictionary for state abbreviations
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


# Bring in data for active NFL players by home state
url = 'https://www.pro-football-reference.com/friv/birthplaces.htm'
html = requests.get(url).content
df_list=pd.read_html(html)
nflstate = df_list[-1]

nflstate = nflstate.drop(nflstate.columns[[0,1,3,5,6,7,8,9,10,11]], axis =1)
nflstate = nflstate.iloc[:52]
nflstate = nflstate.iloc[1:]

print(nflstate)


# Bring in data for us population by state
url = 'https://web.archive.org/web/20101225031104/http://2010.census.gov/2010census/data/apportionment-pop-text.php'
html = requests.get(url).content
df_list = pd.read_html(html)
uspop = df_list[-1]


uspop['State or Region'] = uspop['State or Region'].shift(1)

uspop = uspop.iloc[16:]

uspop = uspop[(uspop.index + 2) % 3 == 0]
uspop = uspop.drop(uspop.columns[[1,2,3,4,5,6,7,8,9,10]], axis=1)

uspop = uspop.replace({"State or Region":us_state_abbrev})

#Join player data and US population data into dataframe finaldf
finaldf = nflstate.join(uspop.set_index('State or Region'),on ='State')
finaldf = finaldf.rename(columns={"# Active": "NumPros", "2010": "UsPop"})

finaldf['PctPlayers']=finaldf['NumPros']/finaldf['NumPros'].sum()
finaldf.UsPop = pd.to_numeric(finaldf.UsPop)
finaldf['PctUSPop']=finaldf['UsPop']/finaldf['UsPop'].sum()
finaldf['Represent']=finaldf['PctPlayers']/finaldf['PctUSPop']

#Build the visualization 

fig = go.Figure(data=go.Choropleth(
        locations = finaldf['State'],
        z = finaldf['Represent'].astype(float),
        locationmode = 'USA-states',
       colorscale ='Reds',
       zmin = 0,
       zmax = 2,
       colorbar_title = "Representation in NFL",
  ))



fig.update_layout(
        title_text='Representation of Active NFL players by state',
        geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes = True,
                lakecolor = 'rgb(255,255,255)'),
   )
        

plot(fig)
           

finaldf.sort_values(by=['Represent'], ascending = False)        
                                


