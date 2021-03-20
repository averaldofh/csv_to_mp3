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
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import webbrowser
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def callback(url):
    webbrowser.open_new(url)

def get_href(url):
    response = requests.get(url)
    content = response.content
    ii = content.find(b'/watch?')
    tag = str(content[ii:ii+20])
    tag = tag[2:-1]
    return tag

def yt_dler(vid_link):
    outpath = str(app.ent_folder.get()+'/%(title)s.%(ext)s')
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

def names(folder):
    for filename in (os.listdir(folder)):
        dst = str(filename).replace('_',' ')
        print('Renaming ', str(filename), ' To ', dst)
        src = folder + '/' + str(filename)
        dst = folder + '/' + dst
        os.rename(src, dst)

def processlist(songlist):
    global m, p
    songs = pd.read_csv(songlist)
    songs.drop_duplicates(subset='Track Name', keep='first', inplace=True, ignore_index=True)
    search_url = 'https://www.youtube.com/results?search_query='
    yt_link = 'http://www.youtube.com'
    m = len(songs["Track Name"])
    i=0
    while i<len(songs["Track Name"]):
        this_song = songs["Track Name"][i]+" "+ songs["Artist Name"][i]
        this_search = "+".join(this_song.strip().split())
        div = get_href(search_url+this_search)
        complete_link = yt_link+div
        yt_dler(complete_link)
        i+=1
        p=i
        UiApp.upd_progress(app)
    if app.ent_folder.get() != '':
        names(app.ent_folder.get())
        UiApp.out_en(app)
    else:
        pass

class UiApp:
    global ico
    def __init__(self, master=None):
        # build ui
        self.mainApp = tk.Tk() if master is None else tk.Toplevel(master)
        self.fr_main = ttk.Frame(self.mainApp)
        self.label1 = ttk.Label(self.fr_main)
        self.label1.configure(font='{Calibri} 20 {bold}', text='CSV Youtube Downloader')
        self.label1.pack(side='top')
        self.lf_input = ttk.Labelframe(self.fr_main)
        self.lbl_input = ttk.Label(self.lf_input)
        self.lbl_input.configure(text='Choose the csv file:')
        self.lbl_input.pack(anchor='w', pady='5', side='top')
        self.ent_input = ttk.Entry(self.lf_input)
        self.ent_input.configure(state='readonly')
        self.ent_input.pack(anchor='n', expand='true', fill='x', ipady='2', pady='5', side='left')
        self.btn_file = ttk.Button(self.lf_input)
        self.btn_file.configure(text='Open...')
        self.btn_file.pack(anchor='n', pady='5', side='right')
        self.btn_file.configure(command=self.cmd_inputfile)
        self.lf_input.configure(height='100', text='Input file (csv)', width='450')
        self.lf_input.pack(side='top')
        self.lf_input.pack_propagate(0)
        self.lf_output = ttk.Labelframe(self.fr_main)
        self.lbl_output = ttk.Label(self.lf_output)
        self.lbl_output.configure(text='Select a folder where to download the songs:')
        self.lbl_output.pack(anchor='w', pady='5', side='top')
        self.ent_folder = ttk.Entry(self.lf_output)
        self.ent_folder.configure(state='readonly')
        self.ent_folder.pack(anchor='n', expand='true', fill='x', ipady='2', pady='5', side='left')
        self.btn_outsel = ttk.Button(self.lf_output)
        self.btn_outsel.configure(text='Choose Folder...')
        self.btn_outsel.pack(anchor='n', pady='5', side='right')
        self.btn_outsel.configure(command=self.cmd_outputpath)
        self.lf_output.configure(height='100', text='Output Folder', width='450')
        self.lf_output.pack(side='top')
        self.lf_output.pack_propagate(0)
        self.fr_main.configure(height='240', width='450')
        self.fr_main.pack(anchor='n', side='top')
        self.fr_main.pack_propagate(0)
        self.fr_actions = ttk.Frame(self.mainApp)
        self.fr_btns = ttk.Frame(self.fr_actions)
        self.btn_dl = ttk.Button(self.fr_btns)
        self.btn_dl.configure(default='disabled', state='disabled', text='Download list')
        self.btn_dl.pack(side='left')
        self.btn_dl.configure(command=self.cmd_dl)
        self.btn_out = ttk.Button(self.fr_btns)
        self.btn_out.configure(default='disabled', state='disabled', text='Open Output')
        self.btn_out.pack(side='right')
        self.btn_out.configure(command=self.cmd_open)
        self.fr_btns.configure(height='25', width='450')
        self.fr_btns.pack(side='top')
        self.fr_pb = ttk.Frame(self.fr_actions)
        self.pb_progress = ttk.Progressbar(self.fr_pb)
        self.pb_progress.configure(orient='horizontal')
        self.pb_progress.pack(fill='x', side='top')
        self.fr_pb.configure(height='20', width='350')
        self.fr_pb.pack(pady='2', side='top')
        self.fr_pb.pack_propagate(0)
        self.fr_footer = ttk.Frame(self.fr_actions)
        self.lbl_ver = ttk.Label(self.fr_footer)
        self.lbl_ver.configure(text='V1.0 -')
        self.lbl_ver.pack(anchor='s', side='left')
        self.lbl_ver.pack_propagate(0)
        self.lbl_git = ttk.Label(self.fr_footer)
        self.lbl_git.configure(cursor='hand2', foreground='#0000ff', text='github.com')
        self.lbl_git.bind("<Button-1>", lambda e: callback("http://www.github.com/averaldofh/csv_to_mp3"))
        self.lbl_git.pack(anchor='s', side='left')
        self.btn_quit = ttk.Button(self.fr_footer)
        self.btn_quit.configure(text='Quit')
        self.btn_quit.pack(anchor='s', side='right')
        self.btn_quit.configure(command=self.cmd_exit)
        self.fr_footer.configure(height='30', width='480')
        self.fr_footer.pack(side='bottom')
        self.fr_footer.pack_propagate(0)
        self.fr_actions.configure(height='80', width='200')
        self.fr_actions.pack(side='top')
        self.mainApp.configure(height='200', width='200')
        self.mainApp.geometry('480x320')
        self.mainApp.iconbitmap(ico)
        self.mainApp.resizable(False, False)
        self.mainApp.title('CSV Youtube Downloader')

        # Main widget
        self.mainwindow = self.mainApp


    def cmd_inputfile(self):
        file = askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.btn_out['state'] = tk.DISABLED
        self.ent_input['state'] = tk.NORMAL
        self.ent_input.delete('0','end')
        self.ent_input.insert('0',file)
        self.pb_progress['value'] = 0

    def cmd_outputpath(self):
        folder = askdirectory()
        self.ent_folder['state'] = tk.NORMAL
        self.ent_folder.delete('0','end')
        self.ent_folder.insert('0',folder)
        if (self.ent_input.get() != '') and (self.ent_folder.get() != ''):
            self.btn_dl['state'] = tk.NORMAL

    def out_en(self):
        self.btn_out['state'] = tk.NORMAL

    def cmd_dl(self):
        pathin = self.ent_input.get()
        processlist(pathin)
        pass

    def cmd_open(self):
        outfolder = self.ent_folder.get()
        outfolder = '"{}"'.format(outfolder)
        os.startfile(outfolder)
        pass

    def cmd_exit(self):
        self.mainApp.quit()
        pass

    def run(self):
        self.mainwindow.mainloop()

    def upd_progress(self):
        global m, p
        self.pb_progress['maximum'] = m
        self.pb_progress['value'] = p
        self.mainApp.update()

if __name__ == '__main__':
    p = 0
    m = 0
    ico = resource_path(r'D:\Python\csv2mp3\ico.ico')
    app = UiApp()
    app.run()
    exit(0)

