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

path_to_df = "./Data/vcounty.csv"
# path_to_df = pkg_resources.resource_filename('county_package', 'Data/vcounty.csv')
fips_df = pd.read_csv(path_to_df, dtype={"county_fips": str})


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
import numpy as np

def plurality(row):
    """
    Determine the party with the highest percentage based on a row of votes.

    Parameters
    ----------
    row : numpy.ndarray
        One-dimensional array representing the percentage of votes for each party.

    Returns
    -------
    str
        The party with the highest percentage of votes.

    Notes
    -----
    The input `row` should be a NumPy array containing the percentage of votes for each party.
    The function calculates the percentage for each party, identifies the party with the
    highest percentage, and returns its name.

    Examples
    --------
    >>> import numpy as np
    >>> row = np.array([30, 20, 50])  # Example percentages for three parties
    >>> plurality(row)
    'Party C'

    """
    # Calculate percentage for each column
    percentages = row / row.sum() * 100
    # Get the party with the highest percentage
    return percentages.argmax()


# Create a new column containing the most voted party for each row
final["most_voted_party"] = final[
    ["REPUBLICAN", "DEMOCRAT", "LIBERTARIAN", "GREEN", "OTHER"]
].apply(plurality, axis=1)

final["common_education"] = final[["noHS", "HS", "someCol", "Col"]].apply(
    plurality, axis=1
)


def stat_sum(final):
    """
    Calculate summary statistics for the given DataFrame.

    Parameters
    ----------
    final : pandas.DataFrame
        The DataFrame containing the data for which summary statistics are to be calculated.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing summary statistics for selected columns.

    Notes
    -----
    This function calculates summary statistics (minimum, maximum, median, mean) for
    specific columns in the input DataFrame.

    - 'total_cost': Total cost column.
    - 'median_family_income': Median family income column.
    - 'REPUBLICAN': Republican column.
    - 'DEMOCRAT': Democrat column.
    - 'noHS': Column representing individuals with no high school education.
    - 'HS': Column representing individuals with a high school education.
    - 'someCol': Column representing individuals with some college education.
    - 'Col': Column representing individuals with a college education.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming 'final' is your DataFrame
    >>> summary_stats = stat_sum(final)
    >>> print(summary_stats)
                     total_cost  median_family_income  ...         someCol            Col
    min          1000.00                25000.00                  ...          30000.00        50000.00
    max        1000000.00            150000.00                  ...       120000.00      200000.00
    median    500000.00                75000.00                  ...        60000.00        90000.00
    mean      550000.00                80000.00                  ...        65000.00        95000.00

    """
    return final.agg(
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
import seaborn as sns
import matplotlib.pyplot as plt

def edu_scat(final):
    """
    Create a scatter plot of Total_cost vs median family income, coloring the points
    based on the plurality of common_education.

    Parameters
    ----------
    final : pandas.DataFrame
        The DataFrame containing the data to be used for creating the scatter plot.

    Notes
    -----
    This function generates a scatter plot of 'total_cost' versus 'median_family_income'.
    The points in the plot are colored based on the plurality of 'common_education' for each
    unique combination of 'county' and 'state_x' in the input DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming 'final' is your DataFrame
    >>> edu_scat(final)

    The resulting scatter plot will be displayed, and the image will be saved to "../Images/incomeVSeducation.png".

    """
    sns.scatterplot(
        x=final.groupby(["county", "state_x"])["total_cost"].mean(),
        y=final.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=final.groupby(["county", "state_x"])["common_education"].first(),
    )
    plt.savefig("../Images/incomeVSeducation.png")
    plt.show()  # If you want to display the plot interactively
import seaborn as sns
import matplotlib.pyplot as plt

def vote_scat(final):
    """
    Create a scatter plot of Total Cost vs Median Family Income, coloring the points
    based on the most common political party in each county.

    Parameters
    ----------
    final : pandas.DataFrame
        The DataFrame containing the data to be used for creating the scatter plot.

    Notes
    -----
    This function generates a scatter plot of 'total_cost' versus 'median_family_income'.
    The points in the plot are colored based on the most common political party ('most_voted_party')
    for each unique combination of 'county' and 'state_x' in the input DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming 'final' is your DataFrame
    >>> vote_scat(final)

    The resulting scatter plot will be displayed, and the image will be saved to "../Images/incomeVSvoting.png".

    """
    sns.scatterplot(
        x=final.groupby(["county", "state_x"])["total_cost"].mean(),
        y=final.groupby(["county", "state_x"])["median_family_income"].mean(),
        hue=final.groupby(["county", "state_x"])["most_voted_party"].first(),
    )
    plt.savefig("../Images/incomeVSvoting.png")
    plt.show()  # If you want to display the plot interactively
import seaborn as sns
import matplotlib.pyplot as plt

def family_size_scat(final):
    """
    Create a scatter plot of Total Cost vs Median Family Income, coloring the points
    based on the family household size.

    Parameters
    ----------
    final : pandas.DataFrame
        The DataFrame containing the data to be used for creating the scatter plot.

    Notes
    -----
    This function generates a scatter plot of 'total_cost' versus 'median_family_income'.
    The points in the plot are colored based on the 'family_member_count' column, representing
    the size of the family household.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming 'final' is your DataFrame
    >>> family_size_scat(final)

    The resulting scatter plot will be displayed, and the image will be saved to "../Images/incomeVSfamilySize.png".

    """
    sns.scatterplot(
        x=final["total_cost"],
        y=final["median_family_income"],
        hue=final["family_member_count"],
    )
    plt.savefig("../Images/incomeVSfamilySize.png")
    plt.show()  # If you want to display the plot interactively

### Graph data on a map
import plotly.express as px

def income_map(cost_piv, counties):
    """
    Create a choropleth map with a color scale to visualize median family income.

    Parameters
    ----------
    cost_piv : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.
    counties : dict
        The GeoJSON data for the counties to be used in the map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying the median
    family income for each county. The map uses a color scale to represent income levels.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> # Assuming 'cost_piv' and 'counties' are your DataFrames
    >>> income_map(cost_piv, counties)

    The resulting choropleth map will be displayed.

    """
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
import pandas as pd
import numpy as np
import plotly.express as px

def cost_map(final):
    """
    Create a choropleth map with a color scale to visualize total cost for a 2-parent 1-child family.

    Parameters
    ----------
    final : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying the total cost
    for a 2-parent 1-child family in each county. The map uses a color scale to represent cost levels.

    Examples
    --------
    >>> import pandas as pd
    >>> # Assuming 'final' is your DataFrame
    >>> cost_map(final)

    The resulting choropleth map will be displayed, and the image will be saved to "cost_map.png".

    """
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
import plotly.express as px

def income_cost_diff_map(cost_piv, counties):
    """
    Create a choropleth map with a color scale to visualize the difference in
    median family income and cost for a 2-parent 1-child family.

    Parameters
    ----------
    cost_piv : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.
    counties : dict
        The GeoJSON data for the counties to be used in the map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying the
    difference in median family income and cost for a 2-parent 1-child family in each county.
    The map uses a color scale to represent the income-cost difference.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> # Assuming 'cost_piv' and 'counties' are your DataFrames
    >>> income_cost_diff_map(cost_piv, counties)

    The resulting choropleth map will be displayed.

    """
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

import plotly.express as px

def Republican_map(fips_df, counties):
    """
    Create a choropleth map with a color scale to visualize the percentage of Republican votes in each county.

    Parameters
    ----------
    fips_df : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.
    counties : dict
        The GeoJSON data for the counties to be used in the map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying the
    percentage of Republican votes in each county. The map uses a color scale to represent
    the Republican vote percentages.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> # Assuming 'fips_df' and 'counties' are your DataFrames
    >>> Republican_map(fips_df, counties)

    The resulting choropleth map will be displayed.

    """
    voting_fig = px.choropleth(
        fips_df,
        geojson=counties,
        locations="county_fips",
        color="REPUBLICAN",
        color_continuous_scale="balance",
        hover_data=["state", "county_name"],
        range_color=(0, 1),
        scope="usa",
        labels={"REPUBLICAN": "% Republican"},
    )
    voting_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    voting_fig.show()
import plotly.express as px

def vote_map(fips_df, counties):
    """
    Create a choropleth map with a color scale to visualize the total number of votes cast in each county.

    Parameters
    ----------
    fips_df : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.
    counties : dict
        The GeoJSON data for the counties to be used in the map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying the
    total number of votes cast in each county. The map uses a color scale to represent
    the voting population.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> # Assuming 'fips_df' and 'counties' are your DataFrames
    >>> vote_map(fips_df, counties)

    The resulting choropleth map will be displayed.

    """
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
import plotly.express as px

def unemployement_map(unemployment, counties):
    """
    Create a choropleth map with a color scale to visualize unemployment rates in each county.

    Parameters
    ----------
    unemployment : pandas.DataFrame
        The DataFrame containing the data for creating the choropleth map.
    counties : dict
        The GeoJSON data for the counties to be used in the map.

    Notes
    -----
    This function generates a choropleth map using Plotly Express, displaying
    unemployment rates in each county. The map uses a color scale to represent
    the percentage of unemployment.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.express as px
    >>> # Assuming 'unemployment' and 'counties' are your DataFrames
    >>> unemployement_map(unemployment, counties)

    The resulting choropleth map will be displayed.

    """
    unemp_chart = px.choropleth(unemployment, geojson=counties, locations='fips', color='unemp',
                            color_continuous_scale="Viridis",
                            range_color=(0, 12),
                            scope="usa",
                            labels={'unemp': '% Unemployment'}
                            )
    unemp_chart.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    unemp_chart.show()

cost_map(final)