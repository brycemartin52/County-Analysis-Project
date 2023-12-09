## Import the necessary packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the csv
data = pd.read_csv('../Data/countyVLivEdu.csv')


def plurality(row):
    # Calculate percentage for each column
    percentages = row / row.sum() * 100
    # Get the party with the highest percentage
    return percentages.idxmax()

# Create a new column containing the most voted party for each row
data['most_voted_party'] = data[['REPUBLICAN', 'DEMOCRAT', 'LIBERTARIAN', 'GREEN', 'OTHER']].apply(plurality, axis=1)
data['common_education'] = data[['noHS', 'HS',	'someCol',	'Col']].apply(plurality, axis=1)

# Display the updated DataFrame
data[['noHS', 'HS',	'someCol',	'Col', 'common_education']]


#data[data['common_education'] == 'noHS']
data['most_voted_party'].value_counts()
data['common_education'].value_counts()
# data

sns.scatterplot(x=data.groupby(['county', 'state_x'])['total_cost'].mean(), 
                y = data.groupby(['county', 'state_x'])['median_family_income'].mean(),
                hue=data.groupby(['county', 'state_x'])['common_education'].first())


sns.scatterplot(x=data.groupby(['county', 'state_x'])['total_cost'].mean(), 
                y = data.groupby(['county', 'state_x'])['median_family_income'].mean(),
                hue=data.groupby(['county', 'state_x'])['most_voted_party'].first())


sns.scatterplot(x=data['total_cost'], 
                y = data['median_family_income'],
                hue=data['family_member_count'])
                

sns.scatterplot(x=data['housing_cost'], 
                y = data['median_family_income'],
                hue=data['family_member_count'])
                