import pandas as pd
from pandas.core.frame import DataFrame


def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)
    

codes_df = pd.read_csv("datasets/country_codes.csv", delimiter=',', encoding="latin1")
bands_df = pd.read_csv("datasets/metal_bands_2017.csv", delimiter=',', encoding="latin1")
world_df = pd.read_csv("datasets/world_population.csv", delimiter=';', encoding="latin1")

# clean column origin
bands_df.dropna(subset=["origin"], inplace=True)

# add new column to the DataFrame based on the count of the origins in the Dataframe
bands_df["frequency"] = bands_df["origin"].map(bands_df["origin"].value_counts())


# sort and remove duplicates while keeping the first record
bands_df.sort_values("origin",inplace=True)
bands_df.drop_duplicates(subset="origin", keep='first', inplace=True)

# discarding irrelevant columns
filterColumns(bands_df,['origin','frequency'])

# Merge with world population DF

output_df = bands_df.merge(world_df, left_on='origin', right_on='country')
filterColumns(output_df,['origin','frequency','population'])

output_df['per_capita'] = output_df['frequency'] / output_df['population']
filterColumns(output_df, ['origin','per_capita'])

output_df = output_df.merge(codes_df, left_on='origin', right_on='name')
filterColumns(output_df, ['per_capita','alpha-2'])

output_df.to_csv('data.csv', index=False, header=True)