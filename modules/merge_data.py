## Import the necessary packages
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re

# Read the education data
edu = pd.read_excel("../Data/Education.xlsx", header=3)

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
kag = pd.read_csv("../Data/cost_of_living_us.csv")
kag

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
merge1.info()

# State Abbreviation
abs = pd.read_csv("../Data/StateAbbvs.csv", header=None)
abs.columns = ["State", "Abv"]
abs.State = abs.State.str.upper()
abs

# County data
vcounty = pd.read_csv("../Data/vcounty.csv")
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
    ]
]

vcounty = pd.merge(vcounty, abs, left_on="state", right_on="State", how="inner")
vcounty = vcounty.drop(columns=["State"])

vcounty.Abv = vcounty.Abv.str.strip()
vcounty.county_name = vcounty.county_name.str.strip()
vcounty.info()

# Final merge
final = pd.merge(
    merge1,
    vcounty,
    left_on=["state", "county"],
    right_on=["Abv", "county_name"],
    how="inner",
)
final.info()

# Write the final csv
final.to_csv("../Data/countyVLivEdu.csv")
