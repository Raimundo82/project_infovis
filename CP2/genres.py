import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

def add_value_to_df(df, id, id_column,column, value):
    index = df.loc[df[id_column]==id].index
    df.loc[index[0], column] = value
    return

artists_path = 'C:\\Users\\Admin\\Documents\\MEIC\\VI\\project_infovis\\project_datasets\\artists.csv'
tracks_path = 'C:\\Users\\Admin\\Documents\\MEIC\\VI\\project_infovis\\project_datasets\\Global_streams.csv'

artists = pd.read_csv(artists_path, delimiter=',', na_values=["", None], na_filter=True, encoding="latin1")
artists.dropna(inplace=True)

tracks = pd.read_csv(tracks_path, delimiter=',', na_values=["", None], na_filter=True, encoding="latin1")

filterColumns(tracks, ['name', 'artist_id','total_streams', 'track_id'])

tracks=pd.DataFrame(tracks.assign(artist_id=tracks.artist_id.str.split(",")).explode('artist_id'))
tracks.tail()
artists=pd.DataFrame(artists.assign(genres=artists.genres.str.split(",")).explode('genres'))
artists.tail()



tracks['artist_id']=tracks.artist_id.str.strip()
artists['genres']=artists.genres.str.strip()


output = artists.merge(tracks, left_on="artist_id", right_on="artist_id")
output.drop_duplicates(keep='first', inplace=True)

genres_df = DataFrame()
genres_df['genre'] = output.genres.unique()

for genre in genres_df['genre'].values:
    add_value_to_df(genres_df, genre, 'genre', 'total_genre_streams', sum(output.loc[output['genres'] == genre]['total_streams']))
    add_value_to_df(genres_df, genre, 'genre', 'number_of_tracks', len(output[output['genres'] == genre]['track_id'].unique()))
    add_value_to_df(genres_df, genre, 'genre', 'number_of_artists', len(output[output['genres'] == genre]['artist_id'].unique()))

genres_df.sort_values('total_genre_streams',ascending=False, inplace=True)

genres_df.to_csv('genres.csv', index=False, header=True)


#genres_df['total_genre_streams'] = genres_df['genre'].map(output['total_streams'].sum())
#genres_df.sort_values("total_genre_streams", ascending=False, inplace=True)

