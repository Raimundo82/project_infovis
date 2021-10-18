from numpy.lib.function_base import average
import pandas as pd
import numpy as np


def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

tracks_df = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',')
artists_df = pd.read_csv('project_datasets/global/global_artists_2017_2020.csv', delimiter=',')

for track in tracks_df.values:
    track_id = track[0]
    artist_id = track[2]
    artists = artist_id.split(",")
    genres = ''
    for a in artists:
        genre = artists_df[artists_df['artist_id'] == a]['genres'].values[0]
        gs = str(genre).split(",")
        for g in gs:
            if g != 'nan':
                genres += str(g) + ',' 
    genres = genres[:-1]
    add_value_to_df(tracks_df, track_id, 'track_id', 'genres', genres)
print(tracks_df.head)
tracks_df.to_csv('project_datasets/global/new_global_tracks_2017_2020.csv', index=False, header=True)