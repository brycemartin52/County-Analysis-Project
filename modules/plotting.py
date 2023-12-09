# Import necessary packages
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px

# Read in data frames
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("../Data/viz_data.csv", dtype={"county_fips": str})

# Create the Republican voting percentage
fig = px.choropleth(df, geojson=counties, locations='county_fips', color='REPUBLICAN',
                           color_continuous_scale="balance",
                           range_color=(0, 1),
                           scope="usa",
                           labels={'Republican':'% Republican'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# Voting percentage graph
fig2 = px.choropleth(df, geojson=counties, locations='county_fips', color='totalvotes',
                           color_continuous_scale="Viridis",
                           hover_data = ["state", "county_name"],
                           range_color=(0, 50000),
                           scope="usa",
                           labels={'totalvotes':'% Voting population'}
                          )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()