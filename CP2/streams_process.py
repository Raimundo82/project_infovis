from numpy import NAN, NaN, ceil
from numpy.lib.function_base import average
import pandas as pd
from pandas.core.frame import DataFrame
from datetime import date

def add_value_to_df(df, id, column, value):
    index = df.loc[df['track_id']==id].index
    df.loc[index[0], column] = value
    return

def get_month(x):
    year =int(x[0:4])
    month = int(x[5:7])
    day = int(x[8:])
    return date(year, month, day).strftime('%B')

path = 'project_datasets/'

streams = pd.read_csv(path + "/streams.csv", delimiter=",",encoding='latin1')

countries = streams.country.unique()

for c in countries:
    df = DataFrame()
    sub_stream = streams[streams['country'] == c]
    songs = sub_stream.song_id.unique()
    df['track_id'] = songs
    for song in songs:
        song_substream = sub_stream[sub_stream['song_id'] == song]
        song_substream['month'] = song_substream.date.map(get_month)
        add_value_to_df(df, song, 'times_in_daily_chart', '%.0f'%(len(song_substream)))
        add_value_to_df(df, song, 'top_peak_pos', min(song_substream['pos']))
        add_value_to_df(df, song, 'avg_chart_pos', round(average(song_substream['pos'])))
        add_value_to_df(df, song, 'total_streams', sum(song_substream['streams']))
        months = song_substream.month.unique()
        for m in months:
            val = sum(song_substream[song_substream['month'] == m]['streams'].values)
            add_value_to_df(df, song, m + '_streams', val)


    df.sort_values('total_streams', ascending=False,inplace=True)
    df.to_csv(path + c + '_streams.csv', index=False, header=True)

#artists_df = pd.read_csv(path + "/artists.csv", delimiter=",",encoding='latin1')
#artists_df['followers'] = artists_df.followers.map(int)
#artists_df.sort_values('followers', ascending=False).to_csv('artists.csv', index=False, header=True)

tracks_df = pd.read_csv(path + "/tracks.csv", delimiter=",",encoding='latin1')

for c in countries:
    if c == 'Global':
        continue
    df = pd.read_csv(path +  c + '_streams.csv',delimiter=",",encoding='latin1')
    df = df.merge(tracks_df, left_on='track_id',right_on='track_id')
    df.drop(['id'], axis=1, inplace=True)
    df.to_csv(path + c + '_streams.csv', index=False, header=True)