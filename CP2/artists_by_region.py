from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

artists_path = 'C:\\Users\\Admin\\Documents\\MEIC\\VI\\project_infovis\\project_datasets\\artists.csv'
tracks_path = 'C:\\Users\\Admin\\Documents\\MEIC\\VI\\project_infovis\\project_datasets\\Global_streams.csv'

artists = pd.read_csv(artists_path, delimiter=',', na_values=["", None], na_filter=True, encoding="latin1")

tracks = pd.read_csv(tracks_path, delimiter=',', na_values=["", None], na_filter=True, encoding="latin1")
tracks=pd.DataFrame(tracks.assign(artist_id=tracks.artist_id.str.split(", ")).explode('artist_id'))

global_artists = pd.DataFrame()
global_artists['artist_id'] = tracks['artist_id'].unique()

global_artists = global_artists.merge(artists, left_on="artist_id", right_on="artist_id")
global_artists = global_artists[['artist_id', 'name', 'genres', 'popularity', 'followers']]

for artist in global_artists['artist_id'].values:
    artist_tracks = tracks[tracks['artist_id'] == artist]
    add_value_to_df(global_artists, artist, 'artist_id', 'total_streams', sum(artist_tracks['total_streams']))
    add_value_to_df(global_artists, artist, 'artist_id', 'daily_chart_times', sum(artist_tracks['times_in_daily_chart']))
    add_value_to_df(global_artists, artist, 'artist_id', 'avg_chart_pos', round(average(artist_tracks['avg_chart_pos'])))
    add_value_to_df(global_artists, artist, 'artist_id', 'top_peak_pos', min(artist_tracks['top_peak_pos']))

global_artists.sort_values('total_streams',ascending=False, inplace=True)
print(global_artists)
global_artists.to_csv("project_datasets\\global_artists.csv", index=False, header=True)
