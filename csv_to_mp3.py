#!/usr/bin/env python3

'''
# csv to mp3 #

### What it does: ###

This simple script takes a .csv list of popular song titles and artist names
and searches youtube for that song, grabs the first link that isn't an ad and
downloads the video and converts it to mp3 using youtube-dl/ffmpeg.

So you can listen to these songs off the [internet] grid!

### Why: ###
Sometimes you don't have an internet connection and this is is an easy & lazy
way to download a couple of offline songs w/o worrying about torrenting
individual songs or using youtube2mp3 for each individual song.

Not recommended for building a large library - intended for getting a few songs to
drag to my watch and dumb phone so I can listen to a couple new songs while out

*Not to be used to download music illegally!*
*Please follow local copyright law & support artists!!*



### *Instructions:* ###
1. Install ffmpeg (https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
2. Install youtube_dl, pandas, and bs4 with "pip3 install packagename"
3. Create a songs.csv in the same directory as this auto_yt_dl with a "song" and "artist" field
   (see current songs.csv for example of what it should look like)
4. Run this "python csv_to_mp3.py" (may take about a minute per song)
5. Drag the music to your offline device, and enjoy!

Note: It really only works for fairly popular songs that are on youtube.


todo:
- figure out how to get a csv output from spotify
- maybe worry about output song names?
- make into .exe?

credit:
https://stackoverflow.com/questions/30825371/extract-audio-equivalent-for-youtubedl-class

requires:
ffmpeg - google how to install it and put it in the same directory as your
all below modules (youtube_dl, pandas, bs4) - install w/ "pip3 install youtube_dl" and etc.

'''
import youtube_dl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

songs_csv = "songs.csv"

def get_href(url):
    response = requests.get(url)
    content = response.content
    ii = content.find(b'/watch?')
    tag = str(content[ii:ii+20])
    tag = tag[2:-1]
    return tag


def yt_dler(vid_link):
    # d/l settings
    ydl_opts = {
        'outtmpl': 'Downloaded_mp3/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'restrictfilenames': True}
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([vid_link])

def names(folder):
    for filename in (os.listdir(folder)):
        dst = str(filename).replace('_',' ')
        print('Renaming ', str(filename), ' To ', dst)
        src = folder + '/' + str(filename)
        dst = folder + '/' + dst
        os.rename(src, dst)

def main():
    print('''
    ########################################################################
    ##    YOUTUBE DOWNLOAD FROM CSV LIST V0.1 - Forked from HarryMaher    ##
    ##      USE EXPORTIFY WEBSITE TO GENERATE THE LIST, RENAME TO         ##
    ##      SONGS.CSV IN THE SAME FOLDER AS THIS SCRIPT, AND RUN IT.      ##
    ##      IT WILL DOWNLOAD THE FIRST SEARCH RESULT FOR THE SONG         ##
    ##                                                          MARCH/21  ##
    ########################################################################
    ''')
    songs = pd.read_csv(songs_csv)
    songs.drop_duplicates(subset='Track Name', keep='first', inplace=True, ignore_index=True)
    search_url = 'https://www.youtube.com/results?search_query='
    yt_link = 'http://www.youtube.com'
    i=0
    while i<len(songs["Track Name"]):
        this_song = songs["Track Name"][i]+" "+ songs["Artist Name"][i]
        this_search = "+".join(this_song.strip().split())
        div = get_href(search_url+this_search)
        complete_link = yt_link+div
        print("Downloading: ", i, this_song, " From: ",complete_link)
        yt_dler(complete_link)
        i+=1
    print('Rename files to avoid ugly underscores')
    names('Downloaded_mp3')

if __name__ == "__main__":
    main()
