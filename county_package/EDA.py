"""
This script generates interactive maps of 
different types to visualize county data
"""
## Import the necessary packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import json
from urllib.request import urlopen
import pkg_resources


# Reading in necessary dataframes
with urlopen(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
) as response:
    counties = json.load(response)


unemployment = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv", dtype={"fips": str})

#path_to_df = pkg_resources.resource_filename('countyPackage', 'Data/vcounty.csv')
fips_df = pd.read_csv('Data/vcounty.csv', dtype={"county_fips": str})


# Tidying portion of clean_data.py
# Read the csv
#path_to_final_df = pkg_resources.resource_filename('countyPackage', "Data/countyVLivEdu.csv")
final = pd.read_csv("Data/countyVLivEdu.csv")

cost_piv = pd.pivot_table(
    final,
    index=["county", "state_y", "median_family_income"],
    columns="family_member_count",
    values=["total_cost"],
 )

cost_piv = cost_piv.droplevel(0, axis=1).reset_index()

cost_piv["median_family_cost"] = np.median(
    cost_piv[
        ["1p0c", "1p1c", "1p2c", "1p3c", "1p4c", "2p0c", "2p1c", "2p2c", "2p3c", "2p4c"]
    ],
    axis=1,
)

cost_piv["income_cost_diff"] = cost_piv["median_family_income"] - cost_piv["2p1c"]

fips_df.state = fips_df.state.str.title()

cost_piv = pd.merge(
    cost_piv,
    fips_df,
    left_on=["county", "state_y"],
    right_on=["county_name", "state"],
    how="inner",
)   

housing_piv = pd.pivot_table(
    final,
    index=["county", "state_y", "median_family_income"],
    columns="family_member_count",
    values=["housing_cost"],
)

housing_piv = housing_piv.droplevel(0, axis=1).reset_index()
housing_piv["median_family_cost"] = np.median(
    housing_piv[
        ["1p0c", "1p1c", "1p2c", "1p3c", "1p4c", "2p0c", "2p1c", "2p2c", "2p3c", "2p4c"]
    ],
    axis=1,
)

housing_piv["income_cost_diff"] = (
    housing_piv["median_family_income"] - housing_piv["2p1c"]
)

fips_df.state = fips_df.state.str.title()
housing_piv = pd.merge(
    housing_piv,
    fips_df,
    left_on=["county", "state_y"],
    right_on=["county_name", "state"],
    how="inner",
)

# data[data['common_education'] == 'noHS']
final["most_voted_party"].value_counts()
final["common_education"].value_counts()

def plurality(row):
    """
    Plurality documentation
    """
    # Calculate percentage for each column
    percentages = row / row.sum() * 100
    # Get the party with the highest percentage
    return percentages.idxmax()

# Create a new column containing the most voted party for each row
final["most_voted_party"] = final[
    ["REPUBLICAN", "DEMOCRAT", "LIBERTARIAN", "GREEN", "OTHER"]
].apply(plurality, axis=1)

final["common_education"] = final[["noHS", "HS", "someCol", "Col"]].apply(
    plurality, axis=1
)


def stat_sum():
    #return summary statistics for the data
    final.agg(
    {
        "total_cost": ["min", "max", "median", "mean"],
        "median_family_income": ["min", "max", "median", "mean"],
        "REPUBLICAN": ["min", "max", "median", "mean"],
        "DEMOCRAT": ["min", "max", "median", "mean"],
        "noHS": ["min", "max", "median", "mean"],
        "HS": ["min", "max", "median", "mean"],
        "someCol": ["min", "max", "median", "mean"],
        "Col": ["min", "max", "median", "mean"],
    }
    )




### Scatterplot graphs
def edu_scat():
    #Create a scatter plot of Total_cost vs median family income, coloring the points with the plurality of common_education
    sns.scatterplot(
        x=final.groupby(["county", "state_x"])["total_cost"].mean(),
        y=final.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=final.groupby(["county", "state_x"])["common_education"].first(),
    )
    plt.savefig("../Images/incomeVSeducation.png")

def vote_scat():
    #make a scatterplot of Total Cost vs Median Family Income with the most common politcal party colored
    sns.scatterplot(
        x=final.groupby(["county", "state_x"])["total_cost"].mean(),
        y=final.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=final.groupby(["county", "state_x"])["most_voted_party"].first(),
    )
    plt.savefig("../Images/incomeVSvoting.png")

def family_size_scat():
    #Create a scatter plot of total cost vs median family income with the color as the family household size
    sns.scatterplot(
        x=final["total_cost"],
        y=final["median_family_income"],
        hue=final["family_member_count"],
    )
    plt.savefig("../Images/incomeVSfamilySize.png")

### Graph data on a map
def income_map():
    #create a choropleth map with a color scale to show median family income
    income = px.choropleth(
        cost_piv,
        geojson=counties,
        locations="county_fips",
        color="median_family_income",
        color_continuous_scale="balance",
        hover_data=["state", "county_name"],
        range_color=(30000, 100000),
        scope="usa",
        labels={"median_family_income": "Median Income"},
    )
    income.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    income.show()


### Graph data on a map
def cost_map(final):
        #create a choropleth map with a color scale to show total cost for a 2parent 1 child family

    cost_piv = pd.pivot_table(
        final,
        index=["county", "state_y", "median_family_income"],
        columns="family_member_count",
        values=["total_cost"],
    )
    cost_piv = cost_piv.droplevel(0, axis=1).reset_index()

    cost_piv["median_family_cost"] = np.median(
        cost_piv[
            ["1p0c", "1p1c", "1p2c", "1p3c", "1p4c", "2p0c", "2p1c", "2p2c", "2p3c", "2p4c"]
        ],
        axis=1,
    )

    cost_piv["income_cost_diff"] = cost_piv["median_family_income"] - cost_piv["2p1c"]
    #path_to_df = pkg_resources.resource_filename('countyPackage', 'Data/vcounty.csv')
    fips_df = pd.read_csv('Data/vcounty.csv', dtype={"county_fips": str})
    fips_df.state = fips_df.state.str.title()

    cost_piv = pd.merge(
        cost_piv,
        fips_df,
        left_on=["county", "state_y"],
        right_on=["county_name", "state"],
        how="inner",
    )   

    cost = px.choropleth(
        cost_piv,
        geojson=counties,
        locations="county_fips",
        color="2p1c",
        color_continuous_scale="balance",
        hover_data=["state", "county_name"],
        range_color=(30000, 100000),
        scope="usa",
        labels={"2p1c": "2p1c Cost"},
    )
    cost.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    cost.show()
    plt.savefig("cost_map.png")


### Graph data on a map
def income_cost_diff_map():
    #create a choropleth map with a color scale to show the difference in Median family income and cost for a 2parent 1 child family

    diff = px.choropleth(
        cost_piv,
        geojson=counties,
        locations="county_fips",
        color="income_cost_diff",
        color_continuous_scale="RdBu",
        hover_data=["state", "county_name"],
        range_color=(-55000, 55000),
        scope="usa",
        labels={"income_cost_diff": "Median income - cost"},
    )
    diff.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    diff.show()

def Republican_map():
    #create a choropleth map with a color scale to show the amount of Republican votes in each county

    voting_fig = px.choropleth(
        fips_df,
        geojson=counties,
        locations="county_fips",
        color="REPUBLICAN",
        color_continuous_scale="balance",
        hover_data=["state", "county_name"],
        range_color=(0, 1),
        scope="usa",
        labels={"Republican": "% Republican"},
    )
    voting_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    voting_fig.show()

def vote_map():
    #create a choropleth map with a color scale to show total number of votes cast in each county
    fig2 = px.choropleth(
        fips_df,
        geojson=counties,
        locations="county_fips",
        color="totalvotes",
        color_continuous_scale="Viridis",
        hover_data=["state", "county_name"],
        range_color=(0, 100000),
        scope="usa",
        labels={"totalvotes": "Voting population"},
    )
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig2.show()


def unemployement_map():
    #create a choropleth map with a color scale to show unemployment rates in each county

    unemp_chart = px.choropleth(unemployment, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope="usa",
                            labels={'unemp':'% Unemployment'}
                            )
    unemp_chart.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    unemp_chart.show()