import pandas as pd
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

path = 'project_datasets/global/'

with open("spotify_api_credentials.yaml","r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    client_id =data['client_id']
    secret = data['secret']

client_credentials_manager = SpotifyClientCredentials(client_id, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create dataframe from the csv file
tracks_df = pd.read_csv(path + "global_tracks_2017_2020.csv", delimiter=',', na_values=["", None], na_filter=True)
tracks_df=pd.DataFrame(tracks_df.assign(artist_id=tracks_df.artist_id.str.split(",")).explode('artist_id'))

length = len(tracks_df.artist_id.unique())
counter = 0
last_pct = 0

artists = []
for id in tracks_df.artist_id.unique():   
    artist_info = sp.artist(id)

    name = artist_info["name"]
    genres = ','.join(artist_info['genres'])
    followers =  int(artist_info["followers"]["total"])
    popularity = int(artist_info["popularity"])

    artists.append([id, name, genres, followers, popularity])

    counter += 1
    pct = round(counter/length*100)
    if pct != last_pct:
        print(f'\x1b[1A\x1b[2K{counter}/{length} => {pct}%')
    last_pct = pct

artists_df = pd.DataFrame(artists, columns= ["artist_id","name", "genres", "followers", "popularity"])
artists_df.to_csv(path + 'global_artists_2017_2020.csv', index=False, header=True)