"""
Does a basic analysis on the combined data frame.
Note: must be run after 'clean_data.py' & 'merge_data.py'
"""

if __name__ == "__main__":

    import pandas as pd 
    import numpy as np 
    import statsmodels.formula.api as smf
    def linReg():

        data = pd.read_csv('../Data/countyVLivEdu.csv')
        mod = smf.ols("total_cost ~ median_family_income + family_member_count : median_family_income + DEMOCRAT + REPUBLICAN + noHS + HS + someCol + Col", data=data).fit()
        mod.summary()