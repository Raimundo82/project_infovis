import pandas as pd
from pandas.core.frame import DataFrame

def add_value_to_df(df, id_col, id, column, value):
    index = df.loc[df[id_col]==id].index
    df.loc[index[0], column] = value
    return

def read_from_csv(csv_path, deli=",", enc="latin1"):
    pd.read_csv(csv_path, delimiter=deli, encoding=enc)

def drop_missing_values(df, df_column, inp=True):
    df.dropna(df_column, inplace=inp)

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

def removeColumns(df, cols_to_remove):  
    df.drop(cols_to_remove, axis=1,inplace=True)

def sort(df, column_name, inp=True):
    df.sort_values(column_name,inplace=inp)

def duplicates_drop(df, df_column, keeping="first", inp=True):
    df.drop_duplicates(df_column, keep=keeping, inplace=inp)

def write_to_csv(df, csv_path, ind=False, head=True):
    df.to_csv(csv_path, index=ind, header=head)

def merge_df(df, with_df, df_column, with_df_column):
   df.merge(with_df, left_on=df_column, right_on=with_df_column) 