from numpy.lib.function_base import append
import pandas as pd

def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

def filterRows(df, column, values):
    for v in values:
        df = df[df[column] != v]
    return df

df = pd.read_csv('dataclean/data/input/world-happiness-report-2021.csv', delimiter=',')

final = [['','root']]
filterColumns(df, ['Country name','Regional indicator'])

region_children = df['Regional indicator'].unique().tolist()

for child in region_children:
    final.append(['root', child])


country_children = df['Country name'].unique().tolist()

for child in country_children:
    parent = df[df['Country name']==child]['Regional indicator'].values[0]
    final.append([parent, child])

new_df = pd.DataFrame(final, columns=['parent','child'])
new_df.to_csv('project_infovis/dendrogram_2/data/h_data.csv', index=False, header=True)
