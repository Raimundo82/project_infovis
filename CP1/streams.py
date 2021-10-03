import pandas as pd
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


with open("spotify_api_credentials.yaml","r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    client_id =data['client_id']
    secret = data['secret']

client_credentials_manager = SpotifyClientCredentials(client_id, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

spcharts_df = pd.read_csv("streams.csv",delimiter=',',encoding="latin1")

songs_id = spcharts_df.song_id.unique()
songs_df = pd.DataFrame()

songs_df['track_id'] = spcharts_df.song_id.unique()

spcharts_df = spcharts_df.drop_duplicates(subset="song_id", keep='first')

songs_df = songs_df.merge(spcharts_df, left_on="track_id", right_on="song_id")
songs_df.sort_values("title",inplace=True)
songs_df.dropna(subset=['title'],inplace=True)
filterColumns(songs_df, ['track_id','title','artist','country'])

#songs_df['popularity'] = ""
songs_df.insert(2,"popularity","")
songs_df.insert(3,"explicty","")
songs_df.insert(4,"duration","")
songs_df.insert(7,"song_name","")
songs_df.insert(8,"artist_name","")


artists_id = []


def extract_elements(arr,key):
    new_arr = []
    for element in arr:
        new_arr.append(element[key])
    return new_arr


#for i in range(len(songs_df['track_id'])):
#    print(songs_df['track_id'][i])
#for id in songs_df['track_id']:
#    song_info = sp.track(id, 'pt')
#    artists_id.append(extract_elements(song_info["artists"],"id"))
#    artists_name.append(extract_elements(song_info["artists"],"name"))
#    popularity.append(song_info['popularity'])
#    duration.append(song_info['duration'])
#    explicity.append(song_info['explicity'])


