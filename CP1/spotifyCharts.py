from os import replace
from types import ClassMethodDescriptorType
from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from datetime import date, timedelta

#create empty arrays for data we're collecting
dates=[]
url_list=[]
final = []

#map site

regions = ["global"]

url_base = "https://spotifycharts.com/regional/{}/daily/"
start_date= date(2017, 1, 1)
end_date= date(2020, 12, 31)

delta= end_date-start_date

for i in range(delta.days+1):
	day = start_date+timedelta(days=i)
	day_string= day.strftime("%Y-%m-%d")
	dates.append(day_string)

def add_url():
    for date in dates:
        c_string = url+date
        url_list.append(c_string)
            
#function for going through each row in each url and finding relevant song info

def song_scrape(x):
    pg = x
    pos = 0
    for tr in songs.find("tbody").findAll("tr"):
        pos += 1
        artist= tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist= artist.replace("by ","").strip()
  
        title= tr.find("td", {"class": "chart-table-track"}).find("strong").text
 
        songid= tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid= songid.split("track/")[1]

        streams= tr.find("td", {"class":"chart-table-streams"}).text
        
        if  "," in streams:
            streams = int(streams.replace(",",""))


        final.append([pos, title, artist, songid, streams, url_date, region])
	

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',}
for r in regions:
    url = url_base.format(r)
    add_url()

#loop through urls to create array of all of our song info
counter = 0
for u in url_list:
    read_pg= requests.get(u,headers=headers)
    sleep(2)
    soup= BeautifulSoup(read_pg.text, "html.parser")
    url_date = u.split("daily/")[1]     
    #region = (u.split("regional/")[1]).split("/daily")[0]
    try:
        songs= soup.find("table", {"class":"chart-table"})
        region = soup.find("div", {"class":"responsive-select-value"}).text
        song_scrape(u)
        counter += 1
        print(counter)
    except:
        print(u)
 
#convert to data frame with pandas for easier data manipulation

final_df = pd.DataFrame(final, columns= ["pos","title", "artist", "track_id", "streams","date", "country"])

#write to csv

final_df.to_csv('global_streams_2017_2020.csv',header= True, index=False)