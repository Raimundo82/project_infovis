import pandas as pd
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


with open("spotify_api_credentials.yaml","r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    client_id =data['client_id']
    secret = data['secret']

def extract_elements(arr,key):
    str = ''
    for element in arr:
        str += element[key] + ',' 
    return str[:-1]

client_credentials_manager = SpotifyClientCredentials(client_id, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create dataframe from the csv file
spcharts_df = pd.read_csv("project_datasets/global/global_streams_2017_2020.csv",delimiter=',',encoding="latin1")

track_ids = spcharts_df.track_id.unique()
tracks = []
 
counter = 0
last_pct = 0
length = len(track_ids)
for id in track_ids:
    counter+=1
    track_info = sp.track(id,'pt')
    audio_features = sp.audio_features([id])[0]

    if track_info != None and audio_features != None:

        name = track_info['name']
        artist_id = extract_elements(track_info["artists"],'id') 
        artist_name = extract_elements(track_info["artists"], 'name')
        popularity = track_info['popularity']
        explicit = track_info['explicit']
        duration_ms = track_info['duration_ms']

        danceability = audio_features['danceability']
        energy = audio_features['energy']
        key = audio_features['key']
        loudness = audio_features['loudness']
        mode = audio_features['mode']
        speechiness = audio_features['speechiness']
        acousticness = audio_features['acousticness']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        valence = audio_features['valence']
        tempo = audio_features['tempo']
        time_signature = audio_features['time_signature']

    tracks.append([id,name,artist_id,artist_name, popularity, explicit,duration_ms, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,time_signature])
    pct = round(counter/length*100)
    if pct != last_pct:
        print(f'\x1b[1A\x1b[2K{counter}/{length} => {pct}%')
    last_pct = pct


tracks_df = pd.DataFrame(tracks, columns= ["track_id","name","artist_id", "artist_name", "popularity", "explicit","duration_ms","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","time_signature"])
tracks_df.to_csv('project_datasets/global/global_tracks_2017_2020.csv', index=False, header=True)