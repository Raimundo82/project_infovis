from numpy.lib.function_base import average
import pandas as pd
import numpy as np


def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

tracks_df = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',')
tracks_df=pd.DataFrame(tracks_df.assign(genres=tracks_df.genres.str.split(",")).explode('genres'))


genres_df = pd.read_csv('project_datasets/global/genre_derived_measures.csv', delimiter=',')

genres = genres_df['genre'].unique()

columns = ['danceability', 'energy', 'tempo', 'valence', 'loudness', 'speechiness', 'liveness', 'acousticness', 'instrumentalness']

for col in columns:
    genres_df[col] = ""

for genre in genres:
    genre_tracks = tracks_df[tracks_df['genres']== genre]
    for col in columns:
        value = round(genre_tracks[[col]].mean(axis=0)[0],2)
        add_value_to_df(genres_df, genre, 'genre', col, value)




genres_df.to_csv('project_datasets/global/new_genre_derived_measures.csv', index=False, header=True)