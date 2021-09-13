import youtube_dl
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import sys
import eyed3, re

songs_csv = "songs.csv"

def get_href(url):
    response = requests.get(url)
    content = response.content
    ii = content.find(b'/watch?')
    tag = str(content[ii:ii+20])
    tag = tag[2:-1]
    return tag

def yt_dler(vid_link, art, trk):
    outpath = str('Downloaded_mp3/' + re.sub(r"[\/:;?]","-",art) + ' - ' + re.sub(r"[\/:;?]","-",trk) + '.%(ext)s')
    ydl_opts = {
        'outtmpl': outpath,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'quiet': True,
        'ignoreerrors' : True,
        'no_warnings' : True,
        'restrictfilenames': True}

    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([vid_link])

def tag_this(art, trk, alb, trknum):
    audiofile = eyed3.load(str('Downloaded_mp3/' + re.sub('[/\;":?]',"-",art) + ' - ' + re.sub('[/\;":?]',"-",trk) + '.mp3'))
    audiofile.tag.artist = art
    audiofile.tag.title = trk
    audiofile.tag.album = alb
    audiofile.tag.track_num = trknum
    audiofile.tag.save()
    
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
    try:
        songs = pd.read_csv(songs_csv)
    except FileNotFoundError:
        print("File 'songs.csv' not found!")
        input("Press <return> to exit")
        quit()
    print("File 'songs.csv' found!")
    if 'Downloaded_mp3' not in os.listdir(os.getcwd()):
        try:
            os.mkdir('Downloaded_mp3')
        except Exception:
            print('Could not create output folder')
            input("Press <return> to exit")
            quit()
    print("Creating Directory 'Downloaded_mp3'... OK")
    songs.drop_duplicates(subset='Track Name', keep='first', inplace=True, ignore_index=True)
    search_url = 'https://www.youtube.com/results?search_query='
    yt_link = 'http://www.youtube.com'
    m = len(songs["Track Name"])
    i=0
    while i<len(songs["Track Name"]):
        print(f'Song {i+1}/{m}...')
        trk = str(songs["Track Name"][i]).title()
        art = str(songs["Artist Name(s)"][i]).title()
        if 'Album Name' in songs:
            alb = str(songs["Album Name"][i]).title()
        else:
            alb = ''
        
        trknum = m
        
        if (f'{art} - {trk}.mp3') not in os.listdir('Downloaded_mp3/'):
            i+=1
            print(f'Downloading song: {art} - {trk}...')
            this_song = re.sub('[/\;":?]',' ', art) + ' ' + re.sub('[/\;":?]',' ', trk)
            this_search = "+".join(this_song.strip().split())
            div = get_href(search_url+re.sub("[!@#$%¨&*():;|\/?]",' ',this_search))
            complete_link = yt_link+div
            print(complete_link)
            yt_dler(complete_link, art, trk)
            #tag_this(art, trk, alb, trknum)
        else:
            print(f"Song '{art} - {trk}.mp3' already Downloaded, skipping")
            i+=1

if __name__ == "__main__":
    main()