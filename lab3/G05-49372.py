from typing import Counter
import pandas as pd
from pandas.core.frame import DataFrame

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

# reading csv files with some filtering regarding missing values 
gdp_df = pd.read_csv('data.csv', delimiter=',', na_filter=True, na_values=['..', " ", None], encoding="latin1")
codes_df = pd.read_csv("country_codes.csv", delimiter=',', encoding="latin1")

gdp_df.info()

# cleaning dataframes
filterColumns(codes_df,['name','alpha-2'])
codes_df.dropna(inplace=True)

gdp_df.drop(['Info'],axis=1,inplace=True)
gdp_df.dropna(inplace=True)

# calculating the sum of gdp for each country
    
gdp_df["sum"] = gdp_df.sum(axis=1)

# discarding all the years columns
filterColumns(gdp_df, ['Country','sum'])

# generating final data frame
output_df = gdp_df.merge(codes_df, left_on='Country', right_on='name')

# reordering columns and sorting by country code
output_df = output_df[['alpha-2','sum']]
output_df.sort_values('alpha-2',inplace=True)

output_df.to_csv('output.csv', index=False, header=True)