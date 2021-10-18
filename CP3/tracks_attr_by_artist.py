from numpy.lib.function_base import average
import pandas as pd
import numpy as np


def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

tracks_df = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',')
tracks_df=pd.DataFrame(tracks_df.assign(artist_id=tracks_df.artist_id.str.split(",")).explode('artist_id'))

artists_df = pd.read_csv('project_datasets/global/global_artists_2017_2020.csv', delimiter=',')

artists = artists_df['artist_id'].unique()

columns = ['danceability', 'energy', 'tempo', 'valence', 'loudness', 'speechiness', 'liveness', 'acousticness', 'instrumentalness']
for col in columns:
    artists_df[col] = ""
for artist in artists:
    artist_tracks = tracks_df[tracks_df['artist_id'] == artist]
    for col in columns:
        value = round(artist_tracks[[col]].mean(axis=0)[0],2)
        add_value_to_df(artists_df, artist, 'artist_id', col, value)

artists_df.to_csv('project_datasets/global/new_global_artists_2017_2020.csv', index=False, header=True)