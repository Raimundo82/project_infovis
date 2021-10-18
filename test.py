from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from datetime import date

from pandas.core.indexes.base import Index

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

streams = pd.read_csv('project_datasets/global/global_streams_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)

streams.dropna(inplace=True)

streams.to_csv('project_datasets/global/new_global_streams_2017_2020.csv', index=False, header=True)



#tracks = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)

#tracks_df = pd.DataFrame(streams['track_id'].unique(), columns=['track_id'])

#tracks_df = tracks_df.merge(tracks, left_on="track_id", #right_on='track_id')
#
#tracks_df.sort_values("popularity", ascending=False, #inplace=True)
#
#new_tracks_df = tracks_df.drop_duplicates(subset=["name",
#"artist_id"], keep="first")
#
#def add_value_to_df(df, id, id_column,column, value):
#    index = df.loc[df[id_column]==id].index
#    df.loc[index[0], column] = value
#    return
#
#new_tracks_df = new_tracks_df[new_tracks_df.index == 1]
#print(new_tracks_df)
#
#new_tracks_df.to_csv('project_datasets/global/new_global_tracks_2017_2020.csv', index=False, header=True)