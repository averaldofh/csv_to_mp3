# csv to mp3 #

# THIS IS A PERSONAL MODIFICATION #
I've found out this script from Harry Maher, but it was 4 years old, and wasn't working for me.
So i made a little modification that worked, but it's not an inteligent way to do it. 
May lead to problems, for sure, but it's working fine. 
To get a csv file from a spotify playlist use the website
https://watsonbox.github.io/exportify/
put it in the script folder and rename it to songs.csv. no changes required
 - OR -
you can simply create a csv file with two columns named 'Track Name' and 'Artist Name'.
In case there is duplicates for the track name, only 1 will be downloaded.

### *Description:* ###

This script takes a .csv file that contains a list of song titles and artist 
names, searches youtube for those songs, grabs links to the songs, and 
downloads videos and converts them to mp3 format.

Allows you to listen to these songs when you don't have internet!

*Not to be used to download music illegally!*
*Please follow local copyright law & support artists*

### *Why:* ###
Sometimes you don't have an internet connection and this is is an easy & lazy
way to download a couple of songs w/o worrying about looking for torrents for
individual songs or tediously going through a list of songs w/ youtube2mp3.

Not recommended for building a large library--made for getting ~5-15 new songs
to drag to an mp3 player to before going on a run or bike ride

### *Instructions:* ###

0. Clone this repo:
```
$ git clone https://github.com/HarryMaher/csv_to_mp3.git
```
1. Install ffmpeg (https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
2. Install youtube_dl, pandas, and bs4 with "pip3 install packagename"
3. Download the csv file of your playlist from exportify website, rename to songs.csv 
and put in the same directory of this script.
4. Run this "python csv_to_mp3.py" (may take about a minute per song)
5. Drag the music to your offline device, and enjoy!
