import pandas as pd
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


with open("spotify_api_credentials.yaml","r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    client_id =data['client_id']
    secret = data['secret']


def add_value_to_df(df, id, column, value):
    index = df.loc[df['artist_id']==id].index
    df.loc[index[0], column] = value
    return

def extract_elements(arr):
    str = ''
    for element in arr:
        str += element + ', ' 
    return str[:-1]

def convert_to_array(val):
    val = val.split(", ")
    val=val[0:len(val)-1]
    print(val)
    return val
    

client_credentials_manager = SpotifyClientCredentials(client_id, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create dataframe from the csv file
tracks_df = pd.read_csv("tracks.csv",delimiter=',',encoding="latin1")

artists_df = pd.DataFrame()

artists_ids = []
for element in tracks_df.artist_id:
    for id in element.split(', '):
        artists_ids.append(id)

artists_df['artist_id'] = artists_ids

artists_df = artists_df.drop_duplicates(subset="artist_id", keep='first')


artists_df['followers'] = ""
artists_df['genres'] = ""
artists_df['popularity'] = ""
artists_df['name'] = ""


for id in artists_df['artist_id']:
    artist_info = sp.artist(id)
    add_value_to_df(artists_df, id, "followers", int(artist_info["followers"]["total"]))
    add_value_to_df(artists_df, id, "popularity", int(artist_info["popularity"]))
    add_value_to_df(artists_df, id, "genres", ', '.join(artist_info['genres']))
    add_value_to_df(artists_df, id, "name", artist_info["name"])
    
artists_df.to_csv('artists.csv', index=False, header=True)