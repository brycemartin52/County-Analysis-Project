"""
Does a basic analysis on the combined data frame.
Note: must be run after 'clean_data.py' & 'merge_data.py'
"""

if __name__ == "__main__":

    import pandas as pd 
    import numpy as np 
    import statsmodels.formula.api as smf
    import pkg_resources
    def linReg(data):
        #path_to_final_df = pkg_resources.resource_filename('countyPackage', "../Data/countyVLivEdu.csv")
        #data = pd.read_csv(path_to_final_df)
        mod = smf.ols("total_cost ~ median_family_income + family_member_count : median_family_income + DEMOCRAT + REPUBLICAN + noHS + HS + someCol + Col", data=data).fit()
        mod.summary()