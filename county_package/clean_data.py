"""
This script  cleans up the county voting, education, and cost of living data sets
"""


## Import the necessary packages
import pandas as pd
import numpy as np
import pkg_resources
def county():


    # Reading the data into dataframes
    #path_to_vote = pkg_resources.resource_filename('county_package', 'Data/countypres_2000-2020.csv')
    vote = pd.read_csv('Data/countypres_2000-2020.csv')
    #path_to_cost = pkg_resources.resource_filename('county_package', 'Data/cost_of_living_us.csv')
    
    cost = pd.read_csv('Data/cost_of_living_us.csv')

    vote = vote[vote.year == 2020]

    # Creating the voting groupby object
    vote = (
    vote.groupby(
            ["year", "state", "county_name", "county_fips", "party", "totalvotes"]
    )["candidatevotes"]
    .sum()
        .reset_index()
    )

    vcounty = pd.pivot_table(
        vote,
        index=["state", "county_name", "totalvotes", "county_fips"],
        columns="party",
        values=["candidatevotes"],
    )
    vcounty = vcounty.droplevel(0, axis=1).reset_index()
    vcounty["county_fips"] = vcounty["county_fips"].astype("int").astype("str")
    vcounty["county_fips"] = vcounty["county_fips"].apply(
        lambda x: "0" + x if len(x) == 4 else x
    )
    vcounty.fillna(0, inplace=True)

    vcounty["fips"] = vcounty["county_fips"].astype("int")
    vcounty["DEMOCRAT"] = vcounty["DEMOCRAT"] / vcounty["totalvotes"]
    vcounty["GREEN"] = vcounty["GREEN"] / vcounty["totalvotes"]
    vcounty["LIBERTARIAN"] = vcounty["LIBERTARIAN"] / vcounty["totalvotes"]
    vcounty["OTHER"] = vcounty["OTHER"] / vcounty["totalvotes"]
    vcounty["REPUBLICAN"] = vcounty["REPUBLICAN"] / vcounty["totalvotes"]

    vcounty = vcounty.applymap(lambda s: s.title() if type(s) == str else s)

    vcounty = vcounty[
        [
            "state",
            "county_name",
            "totalvotes",
            "DEMOCRAT",
            "GREEN",
            "LIBERTARIAN",
            "OTHER",
            "REPUBLICAN",
            "county_fips"
        ]
    ]

    # State Abbreviation
    path_to_abs = pkg_resources.resource_filename('county_package', "Data/StateAbbvs.csv")
    abs = pd.read_csv(path_to_abs, header=None)
    abs.columns = ["State", "Abv"]
    abs.State = abs.State.str.title()

    abs

    vcounty = pd.merge(vcounty, abs, left_on="state", right_on="State", how="left")

    vcounty.Abv = vcounty.Abv.str.strip()
    vcounty.county_name = vcounty.county_name.str.strip()

    vcounty.to_csv("Data/vcounty.csv")

    edu = pd.read_excel("Data/Education.xlsx", header=3)

    edu = edu[edu["State"] != "PR"]

    edu = edu[
        [
            "State",
            "Area name",
            "Percent of adults with less than a high school diploma, 2017-21",
            "Percent of adults with a high school diploma only, 2017-21",
            "Percent of adults completing some college or associate's degree, 2017-21",
            "Percent of adults with a bachelor's degree or higher, 2017-21",
        ]
    ]
    edu.columns = ["State", "county_name", "noHS", "HS", "someCol", "Col"]

    # Read the kaggle data
    path_to_kag = pkg_resources.resource_filename('county_package', "Data/cost_of_living_us.csv")
    kag = pd.read_csv(path_to_kag)
    #kag

    # Merge the data
    merge1 = pd.merge(
        kag,
        edu,
        left_on=["county", "state"],
        right_on=["county_name", "State"],
        how="inner",
    )   
    merge1 = merge1.drop(columns=["State", "county_name"])
    merge1.county = merge1.county.str.replace(" County", " ")
    merge1.county = merge1.county.str.replace(" Parish", " ")
    merge1.county = merge1.county.str.strip()


    # Final merge
    final = pd.merge(
        merge1,
        vcounty,
        left_on=["state", "county"],
        right_on=["Abv", "county_name"],
        how="inner",
    )


    # Write the final csv
    final.to_csv("Data/countyVLivEdu.csv")
    return final
    # cost_piv.to_csv("../Data/cost_piv.csv")
    # housing_piv.to_csv("../Data/housing_piv.csv")
