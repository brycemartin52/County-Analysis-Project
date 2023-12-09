## Import the necessary packages
import pandas as pd

# Reading the data into dataframes
vote = pd.read_csv("../Data/countypres_2000-2020.csv")
cost = pd.read_csv("../Data/cost_of_living_us.csv")
vote = vote[vote.year == 2020]
vote

#Creating the voting groupby object
vote = vote.groupby(["year","state", "county_name", "county_fips", "party", "totalvotes"])["candidatevotes"].sum().reset_index()


vote.party.unique()
# There's not so many parties that we can't reduce the row count by combining the parties onto one county

vcounty = pd.pivot_table(vote, index=["state", "county_name", "totalvotes", "county_fips"], columns="party", values=["candidatevotes"])
vcounty = vcounty.droplevel(0, axis = 1).reset_index()
vcounty["county_fips"] = vcounty["county_fips"].astype('int').astype('str')
vcounty["county_fips"] = vcounty["county_fips"].apply(lambda x: "0" + x if len(x) == 4 else x)
vcounty.fillna(0, inplace=True)

vcounty["fips"] = vcounty["county_fips"].astype('int')
vcounty["DEMOCRAT"] = vcounty["DEMOCRAT"]/vcounty["totalvotes"]
vcounty["GREEN"] = vcounty["GREEN"]/vcounty["totalvotes"]
vcounty["LIBERTARIAN"] = vcounty["LIBERTARIAN"]/vcounty["totalvotes"]
vcounty["OTHER"] = vcounty["OTHER"]/vcounty["totalvotes"]
vcounty["REPUBLICAN"] = vcounty["REPUBLICAN"]/vcounty["totalvotes"]

vcounty = vcounty.applymap(lambda s: s.title() if type(s) == str else s)

vcounty.to_csv("../Data/viz_data.csv", index = False)