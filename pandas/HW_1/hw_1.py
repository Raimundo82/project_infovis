import pandas as pd
from pandas.core.frame import DataFrame

def add_value_to_df(df, reference_column, reference_value, column, value):
    index = df.loc[df[reference_column]==reference_value].index
    df.loc[index[0], column] = value
    return

arrests_df = pd.read_csv("data.csv", delimiter=',', encoding="latin1")

county_arrests_df = DataFrame()
county_arrests_df['County'] = arrests_df.County.unique()

year_arrests_df = DataFrame()
year_arrests_df['Year'] = arrests_df.Year.unique()

cols_to_calculate_avg = arrests_df.columns
cols_to_calculate_avg =  cols_to_calculate_avg.drop(['Year','County'])

#print(arrests_df[arrests_df['County'] == 'Unknown NYC county']['Year'].values)
#print(len(arrests_df[arrests_df['County'] == 'Albany']['Year'].values))

for county in county_arrests_df['County']:
    for col in cols_to_calculate_avg:
        years = arrests_df[arrests_df['County'] == county]['Year'].values
        initial_value = 0
        for year in years:
            index = arrests_df[arrests_df['Year'] == year][arrests_df['County'] == county].index
            initial_value += arrests_df[col][index].values[0]
        add_value_to_df(county_arrests_df, 'County', county, col, round(initial_value/len(years)))

county_arrests_df.to_csv("avg_arrests_by_county.csv",index=False, header=True)

for year in year_arrests_df['Year']:
    for col in cols_to_calculate_avg:
        counties = arrests_df[arrests_df['Year'] == year]['County'].values
        initial_value = 0
        for county in counties:
            index = arrests_df[arrests_df['County'] == county][arrests_df['Year'] == year].index
            initial_value += arrests_df[col][index].values[0]
        add_value_to_df(year_arrests_df, 'Year', year, col, round(initial_value/len(counties)))

year_arrests_df.to_csv("avg_arrests_by_year.csv",index=False, header=True)
#
#arrests_by_year_df = DataFrame()
#arrests_by_year_df['Year'] = arrests_df['Year'].unique()
#print(arrests_by_year_df.head)
#
#for year in arrests_df['Year'].values:
#    indexes = arrests_df[arrests_df['Year'] == year].index
#    sum = 0
#    for i in indexes.values:
#        sum += arrests_df['Total'][i]
#    add_value_to_df(arrests_by_year_df, year, 'Total',int(sum))
#
#arrests_by_year_df.to_csv("arrests_year.csv",index=False, header=True)
#   
#


