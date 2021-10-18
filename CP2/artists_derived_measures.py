from numpy.lib.function_base import average
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from datetime import date

def filterColumns(df, cols_to_maintain):
    cols_to_remove = [*df.columns]
    for c in cols_to_maintain:
        cols_to_remove.remove(c)    
    df.drop(cols_to_remove, axis=1,inplace=True)

def get_month(date):
    return int(date[5:7])

def get_year(date):
    return int(date[0:4])

def derived_measures(df, array):
    if len(df) > 0:
        chart_presences = len(df)
        avg_rank = round(average(df['pos']))
        array.append(sum(df['streams']))
        array.append(chart_presences)
        array.append(avg_rank)
        array.append(chart_presences * (201 - avg_rank))
        array.append(min(df['pos']))

    else:
        array.append(0)
        array.append(0)
        array.append(0)
        array.append(0)
        array.append(0)

def add_columns(array, year=None,month=None):
    if year==None and month==None:
        array.append("all_streams")
        array.append("all_daily_chart_presences") 
        array.append("all_avg_rank")
        array.append("all_chart_points")
        array.append("all_top_chart_rank")
    elif year != None and month==None:
        array.append(str(year) + "_streams")
        array.append(str(year) + "_daily_chart_presences")
        array.append(str(year) + "_avg_rank")
        array.append(str(year) + "_chart_points")
        array.append(str(year) + "_top_chart_rank")
    else:
        array.append(str(year) + "_" + str(month) + "_streams")
        array.append(str(year) + "_" + str(month) + "_daily_chart_presences")
        array.append(str(year) + "_" + str(month) + "_avg_rank")
        array.append(str(year) + "_" + str(month) + "_chart_points")
        array.append(str(year) + "_" + str(month) + "_top_chart_rank")

tracks = pd.read_csv('project_datasets/global/global_tracks_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)
tracks=pd.DataFrame(tracks.assign(artist_id=tracks.artist_id.str.split(",")).explode('artist_id'))

artists = pd.read_csv('project_datasets/global/global_artists_2017_2020.csv', delimiter=',', na_values=["", None], na_filter=True)
filterColumns(artists, ['artist_id','name'])
artists.drop_duplicates(inplace=True)

streams = pd.read_csv('project_datasets/global/global_streams_2017_2020.csv', delimiter=",")
streams['month'] = streams.date.map(get_month)
streams['year'] = streams.date.map(get_year)

final = []
columns = []

counter = 0
last_pct = 0

length = len(artists)

for row in artists.values:
    id = row[0]
    name = row[1]
    artist_tracks=tracks[tracks['artist_id'] == id]
    track_streams = artist_tracks.merge(streams, left_on="track_id", right_on="track_id")
    artist_arr = []
    artist_arr.append(id)
    artist_arr.append(name)
    derived_measures(track_streams, artist_arr)

    if counter == 0:
        columns.append("artist_id")
        columns.append("artist_name")

        add_columns(columns)

    for year in range(2017,2021):

        if counter == 0:
            add_columns(columns, year=year)

        artist_by_year = track_streams[track_streams['year'] == year]
        derived_measures(artist_by_year, artist_arr)

        for month in range(1,13):
            if counter == 0:
                add_columns(columns, year=year, month=month)

            artist_by_month = artist_by_year[artist_by_year['month'] == month]

            derived_measures(artist_by_month, artist_arr)
    final.append(artist_arr)
    counter += 1
    pct = round(counter/length*100)
    if pct != last_pct:
        print(f'\x1b[1A\x1b[2K{counter}/{length} => {pct}%')
    last_pct = pct


artists_derived_measures = pd.DataFrame(final, columns=columns)
artists_derived_measures.sort_values('all_chart_points', ascending=False, inplace=True)

artists_derived_measures.to_csv("project_datasets/global/artists_derived_measures.csv",index=False,header=True)
