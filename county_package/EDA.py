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
import pkg_resources
from urllib.request import urlopen

# Read the csv
data = pd.read_csv("../Data/countyVLivEdu.csv")

# pkg_resources... ('modules', '../Data/cou...')


def plurality(row):
    """
    Plurality documentation
    """
    # Calculate percentage for each column
    percentages = row / row.sum() * 100
    # Get the party with the highest percentage
    return percentages.idxmax()


if __name__ == '__main__':

    # Create a new column containing the most voted party for each row
    data["most_voted_party"] = data[
        ["REPUBLICAN", "DEMOCRAT", "LIBERTARIAN", "GREEN", "OTHER"]
    ].apply(plurality, axis=1)
    data["common_education"] = data[["noHS", "HS", "someCol", "Col"]].apply(
        plurality, axis=1
    )

    # Display the updated DataFrame
    data[["noHS", "HS", "someCol", "Col", "common_education"]]


    # data[data['common_education'] == 'noHS']
    data["most_voted_party"].value_counts()
    data["common_education"].value_counts()
    # data

    data.agg(
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

    sns.scatterplot(
        x=data.groupby(["county", "state_x"])["total_cost"].mean(),
        y=data.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=data.groupby(["county", "state_x"])["common_education"].first(),
    )
    plt.savefig("../Images/incomeVSeducation.png")

    sns.scatterplot(
        x=data.groupby(["county", "state_x"])["total_cost"].mean(),
        y=data.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=data.groupby(["county", "state_x"])["most_voted_party"].first(),
    )
    plt.savefig("../Images/incomeVSvoting.png")

    sns.scatterplot(
        x=data["total_cost"],
        y=data["median_family_income"],
        hue=data["family_member_count"],
    )
    plt.savefig("../Images/incomeVSfamilySize.png")


    data_piv = pd.pivot_table(
        data,
        index=["county", "state_y", "median_family_income"],
        columns="family_member_count",
        values=["total_cost"],
    )

    data_piv = data_piv.droplevel(0, axis=1).reset_index()
    data_piv["median_family_cost"] = np.median(
        data_piv[
            ["1p0c", "1p1c", "1p2c", "1p3c", "1p4c", "2p0c", "2p1c", "2p2c", "2p3c", "2p4c"]
        ],
        axis=1,
    )

    data_piv["income_cost_diff"] = data_piv["median_family_income"] - data_piv["2p1c"]

    fips_df = pd.read_csv("../Data/viz_data.csv", dtype={"county_fips": str})
    fips_df.state = fips_df.state.str.upper()
    data_piv = pd.merge(
        data_piv,
        fips_df,
        left_on=["county", "state_y"],
        right_on=["county_name", "state"],
        how="inner",
    )
    data_piv


    housing_piv = pd.pivot_table(
        data,
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

    fips_df = pd.read_csv("../Data/viz_data.csv", dtype={"county_fips": str})
    fips_df.state = fips_df.state.str.upper()
    housing_piv = pd.merge(
        housing_piv,
        fips_df,
        left_on=["county", "state_y"],
        right_on=["county_name", "state"],
        how="inner",
    )
    housing_piv

    with urlopen(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    ) as response:
        counties = json.load(response)

    ### Graph data on a map
    income = px.choropleth(
        data_piv,
        geojson=counties,
        locations="county_fips",
        color="median_family_income",
        color_continuous_scale="balance",
        range_color=(30000, 100000),
        scope="usa",
        labels={"median_family_income": "Median Income"},
    )
    income.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    income.show()

    ### Graph data on a map
    cost = px.choropleth(
        data_piv,
        geojson=counties,
        locations="county_fips",
        color="2p1c",
        color_continuous_scale="balance",
        range_color=(30000, 100000),
        scope="usa",
        labels={"2p1c": "2p1c Cost"},
    )
    cost.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    cost.show()

    ### Graph data on a map
    diff = px.choropleth(
        data_piv,
        geojson=counties,
        locations="county_fips",
        color="income_cost_diff",
        color_continuous_scale="RdBu",
        range_color=(-55000, 55000),
        scope="usa",
        labels={"income_cost_diff": "Median income - cost"},
    )
    diff.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    diff.show()
