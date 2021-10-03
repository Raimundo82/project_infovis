import pandas as pd
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


with open("spotify_api_credentials.yaml","r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    client_id =data['client_id']
    secret = data['secret']

def add_value_to_df(df, column_value, column, value):
    index = df.loc[df['track_id']==column_value].index
    df.loc[index[0], column] = value

client_credentials_manager = SpotifyClientCredentials(client_id, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create dataframe from the csv file
spcharts_df = pd.read_csv("streams.csv",delimiter=',',encoding="latin1")

# obtain the unique tracks id
track_id = spcharts_df.song_id.unique()

# create new DF to store all the tracks info
tracks_df = pd.DataFrame()
tracks_df['track_id'] = spcharts_df.song_id.unique()

# add columns

tracks_df['popularity'] = ""
tracks_df['explicit'] = ""
tracks_df['name'] = ""
tracks_df['popularity'] = ""
tracks_df['artist_name'] = ""
tracks_df['artist_id'] = ""

id = "3AEZUABDXNtecAOSC1qTfo"
#id = "51Ss1yLa32T4zi3C82QkZF"
features_columns = sp.audio_features([id])
features = []

for k in features_columns[0]:
    features.append(k)
    tracks_df[k] = ""

keys = tracks_df.columns.drop(['track_id',*features])

def extract_elements(arr,key):
    str = ''
    for element in arr:
        str += element[key] + ', ' 
    return str[:-2]
    
counter = 0
for id in tracks_df['track_id']:
    counter+=1
    track_info = sp.track(id,'pt')
    audio_features = sp.audio_features([id])[0]

    if track_info != None:
        for k in keys:
            if "artist" in k:
                add_value_to_df(tracks_df, id, k, extract_elements(track_info["artists"],k.split("_")[1]))
            else:
                add_value_to_df(tracks_df, id, k, track_info[k])

    if audio_features != None:
        for f in features:
            add_value_to_df(tracks_df, id, f, audio_features[f])
    
tracks_df.drop(['track_href','analysis_url','type','uri'], axis=1, inplace=True)
tracks_df.to_csv('tracks.csv', index=False, header=True)
