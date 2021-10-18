from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

artists = pd.read_csv('project_datasets/global/global_artists_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)

tracks = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)

tracks=pd.DataFrame(tracks.assign(artist_id=tracks.artist_id.str.split(",")).explode('artist_id'))

for artist in artists['artist_id'].values:
    artist_tracks = tracks[tracks['artist_id'] == artist]
    add_value_to_df(artists, artist, 'artist_id', 'all_streams', sum(artist_tracks['all_streams']))
    add_value_to_df(artists, artist, 'artist_id', 'all_daily_chart_presences', sum(artist_tracks['times_in_daily_chart']))
    add_value_to_df(artists, artist, 'artist_id', 'all_avg_chart_pos', round(average(artist_tracks['avg_chart_pos'])))
    add_value_to_df(artists, artist, 'artist_id', 'top_peak_pos', min(artist_tracks['top_peak_pos']))

artists.sort_values('all_streams',ascending=False, inplace=True)
print(artists)
#global_artists.to_csv("project_datasets\\global_artists.csv", index=False, header=True)
