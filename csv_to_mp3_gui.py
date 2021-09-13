'''
1. Install ffmpeg (https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg)
2. Install youtube_dl, pandas, and bs4 with "pip3 install packagename"
3. Export the playlists from spotify using Exportify website
4. Open the exported playlist, choose a download folder and click process
5. Drag the music to your offline device, and enjoy!

credit:
original code by https://github.com/HarryMaher
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
import eyed3, re

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
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

def yt_dler(vid_link, art, trk):
    outpath = str(app.ent_folder.get() + '/' + re.sub("[\/:;?]","-",art) + ' - ' + trk + '.%(ext)s')
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
    audiofile = eyed3.load(str(app.ent_folder.get() + '/' + re.sub("[\/;:?]","-",art) + ' - ' + re.sub("[\/:;?]","-",trk) + '.mp3'))
    audiofile.tag.artist = art
    audiofile.tag.title = trk
    audiofile.tag.album = alb
    audiofile.tag.track_num = trknum
    audiofile.tag.save()

def processlist(songlist):
    global m, p, id3
    songs = pd.read_csv(songlist)
    songs.drop_duplicates(subset='Track Name', keep='first', inplace=True, ignore_index=True)
    search_url = 'https://www.youtube.com/results?search_query='
    yt_link = 'http://www.youtube.com'
    m = len(songs["Track Name"])
    i=0
    UiApp.upd_progress(app)
    while i<len(songs["Track Name"]):
        p=i+1
        UiApp.upd_progress(app)
        trk = str(songs["Track Name"][i]).title()
        if trk.find('- '):
            trk = trk[:trk.find('- ')]
        # trk = re.sub("[\/?:;|]",' ', trk)
        art = str(songs["Artist Name(s)"][i]).title()
        # art = re.sub("[\/?:;|]",' ', art)
        if 'Album Name' in songs:
            alb = str(songs["Album Name"][i]).title()
        else:
            alb = ''
        trknum = m
        if (f'{art} - {trk}.mp3') not in os.listdir(app.ent_folder.get()):
            i+=1
            this_song = re.sub("[\/?:;|]",' ', art) + ' ' + re.sub("[\/?:;|]",' ', trk)
            this_search = "+".join(this_song.strip().split())
            div = get_href(search_url+re.sub("[!@#$%¨&*():;|\/?]",' ',this_search))
            complete_link = yt_link+div
            yt_dler(complete_link, art, trk)
            if id3 == '1':
                tag_this(art, trk, alb, trknum)
        else:
            i+=1
        UiApp.upd_progress(app)
    p=m
    UiApp.upd_progress(app)    
    if app.ent_folder.get() != '':
        UiApp.out_en(app)
    else:
        pass

class UiApp:
    def __init__(self, master=None):
        version = "v0.6"
        # build ui
        self.mainApp = tk.Tk() if master is None else tk.Toplevel(master)
        self.fr_main = ttk.Frame(self.mainApp)
        self.label1 = ttk.Label(self.fr_main)
        self.label1.configure(font='{Calibri} 20 {bold}', text='CSV Youtube Downloader')
        self.label1.pack(side='top')
        self.lbl_instruc = ttk.Label(self.fr_main)
        self.lbl_instruc.configure(font='{Calibri} 10 {}', text='Instructions:')
        self.lbl_instruc.pack(anchor='w', side='top')
        self.lbl_steps = ttk.Label(self.fr_main)
        self.lbl_steps.configure(text='''1. Install FFMPEG!!!
2. Export playlist on Exportify
3. Open exported file
4. Choose where to save the songs''')
        self.lbl_steps.pack(anchor='nw', side='top')
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
        self.fr_actions = ttk.Frame(self.mainApp)
        self.fr_btns = ttk.Frame(self.fr_actions)
        self.btn_out = ttk.Button(self.fr_btns)
        self.btn_out.configure(default='disabled', state='disabled', text='Open Output')
        self.btn_out.pack(side='right')
        self.btn_out.configure(command=self.cmd_open)
        self.btn_dl = ttk.Button(self.fr_btns)
        self.btn_dl.configure(default='disabled', state='disabled', text='Download list')
        self.btn_dl.pack(side='right')
        self.btn_dl.configure(command=self.cmd_dl)
        self.chkbtn_id3 = tk.Checkbutton(self.fr_btns)
        idopt = tk.BooleanVar(name='id3option')
        self.chkbtn_id3.configure(offvalue='0', onvalue='1', state='normal', text='ID3 TAGS')
        self.chkbtn_id3.configure(variable=idopt)
        self.chkbtn_id3.pack(anchor='e', side='left')
        self.chkbtn_id3.configure(command=self.cmd_id3)
        self.fr_btns.configure(height='25', width='450')
        self.fr_btns.pack(side='top')
        self.fr_pb = ttk.Frame(self.fr_actions)
        self.pb_progress = ttk.Progressbar(self.fr_pb)
        self.pb_progress.configure(orient='horizontal')
        self.pb_progress.pack(expand='true', fill='x', side='left')
        self.pb_progress.pack_propagate(0)
        self.lbl_progress = ttk.Label(self.fr_pb)
        self.lbl_progress.configure(font='{calibri} 10 {}', justify='right', text='0/0')
        self.lbl_progress.pack(side='right')
        self.lbl_progress.pack_propagate(0)
        self.fr_pb.configure(height='20', width='350')
        self.fr_pb.pack(pady='2', side='top')
        self.fr_pb.pack_propagate(0)
        self.fr_footer = ttk.Frame(self.fr_actions)
        self.lbl_ver = ttk.Label(self.fr_footer)
        self.lbl_ver.configure(text=version + ' -')
        self.lbl_ver.pack(anchor='s', side='left')
        self.lbl_ver.pack_propagate(0)
        self.lbl_git = ttk.Label(self.fr_footer)
        self.lbl_git.configure(font='{Calibri} 10 {underline}', cursor='hand2', foreground='#0000ff', text='github.com')
        self.lbl_git.pack(anchor='s', side='left')
        self.lbl_git.bind('<1>', lambda e: callback("http://www.github.com/averaldofh/csv_to_mp3"), add='')
        self.lbl_exportify = ttk.Label(self.fr_footer)
        self.lbl_exportify.configure(font='{Calibri} 10 {underline}',cursor='hand2', foreground='#0000ff', text='Exportify')
        self.lbl_exportify.pack(anchor='s', padx='10', side='left')
        self.lbl_exportify.bind('<1>', lambda e: callback("https://watsonbox.github.io/exportify/"), add='')
        self.lbl_ffmpeg = ttk.Label(self.fr_footer)
        self.lbl_ffmpeg.configure(font='{Calibri} 10 {underline}',cursor='hand2', foreground='#0000ff', text='FFMPEG')
        self.lbl_ffmpeg.pack(anchor='s', side='left')
        self.lbl_ffmpeg.bind('<1>', lambda e: callback("https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg"), add='')
        self.btn_quit = ttk.Button(self.fr_footer)
        self.btn_quit.configure(text='Quit')
        self.btn_quit.pack(anchor='s', side='right')
        self.btn_quit.configure(command=self.cmd_exit)
        self.fr_footer.configure(height='30', width='480')
        self.fr_footer.pack(side='bottom')
        self.fr_footer.pack_propagate(0)
        self.fr_actions.configure(height='80', width='200')
        self.fr_actions.pack(side='top')
        self.mainApp.iconbitmap(resource_path('ico.ico'))
        self.mainApp.resizable(False, False)
        self.mainApp.title('CSV Youtube Downloader - ' + version)

        # Main widget
        self.mainwindow = self.mainApp

    def cmd_id3(self):
        global id3
        id3 = self.chkbtn_id3.getvar(name='id3option')

    def cmd_inputfile(self):
        file = askopenfilename(filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.btn_out['state'] = tk.DISABLED
        self.ent_input['state'] = tk.NORMAL
        self.ent_input.delete('0','end')
        self.ent_input.insert('0',file)
        self.ent_input['state'] = 'readonly'
        self.pb_progress['value'] = 0

    def cmd_outputpath(self):
        folder = askdirectory()
        self.ent_folder['state'] = tk.NORMAL
        self.ent_folder.delete('0','end')
        self.ent_folder.insert('0',folder)
        self.ent_folder['state'] = 'readonly'
        if (self.ent_input.get() != '') and (self.ent_folder.get() != ''):
            self.btn_dl['state'] = tk.NORMAL

    def out_en(self):
        self.btn_out['state'] = tk.NORMAL
        self.lbl_progress['text'] = 'Done!'

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
        pgr = "{} / {}".format(p,m)
        self.lbl_progress['text'] = pgr
        self.mainApp.update()

if __name__ == '__main__':
    p = 0
    m = 0
    ico = resource_path(r'D:\Python\csv2mp3\ico.ico')
    app = UiApp()
    app.run()

