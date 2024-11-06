import os, shutil
import asyncio, time
import json

import yt_dlp
from spotdl import Spotdl
from mutagen.easyid3 import EasyID3

import customtkinter as CT 

version = "3.1.0 pre-release"

settings = {
    'Language': 'EN',
    'Threads': 2,    
    'Client_id_spotify': "",
    'Client_secret_spotify': "",
}

CurrentDownloading = {
    "Name": "",
    "Dir": "",
    "Links": ""
}

inputQuary = []

CMDpath = os.getcwd()

willDownload = False

def LoadJson(Loc):
    with open(f'{CMDpath}/bin/{Loc}', 'r') as openfile:
        return json.load(openfile)

def SaveJson(Json, Loc):
    json_object = json.dumps(Json, indent=4)

    with open(f"{CMDpath}/bin/{Loc}", "w") as outfile:
        outfile.write(json_object)


if not os.path.isdir(f'{CMDpath}/bin'):
    os.mkdir(f"{CMDpath}/bin")
    os.mkdir(f"{CMDpath}/bin/Saved")
    f = open(f"{CMDpath}/bin/setting.json", "x")
    f.close()
    SaveJson(settings, 'setting.json')


def SpotifySideDownload(List):
    print('Starting Spotify download')
    DownloadOptions = {
        "threads": int(settings['Threads']),
        "output": CMDpath + "/{artists} - {title}.{output-ext}",
        "max_retries": 5,
    }
    Sdl = Spotdl(client_id=settings['Client_id_spotify'], client_secret=settings['Client_secret_spotify'], downloader_settings=DownloadOptions, no_cache=True) #Threads=int(settings['Threads'])

    song_objs = Sdl.search(List)
    for x in song_objs:
        Putbackthismusic.append(f'{x.artist} - {x.name}.mp3')
        
    Sdl.download_songs(song_objs)
    
    print("Spotify download has finished")

def YoutubeSideDownload(List):
    ytdlp_opts = {
        'format': 'bestaudio/best',
        'skip-unavailable-fragments': True,
        'addmetadata': True,
        'outtmpl': f'{CMDpath}/%(title)s.%(ext)s',
        'ignoreerrors': True,

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

    }

    with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
        ytdl.download(List)
    print("Youtube download has finished")

def ExtractYoutube(link):
    options = {
        'skip_download': True,
        "extract_flat": "in_playlist",
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        playlist_dict = ydl.extract_info(link, download=False)

    urls = []

    json_object = json.dumps(playlist_dict, indent=4)

    with open(f"test.json", "w") as outfile:
        outfile.write(json_object)

    for x in playlist_dict['entries']:
        urls.append(x['url'])

    return urls

def MoveMp3Files(OldFolderPATH, NewFolderPATH, AlbumName):
    try:
        print("trying")
        for song in os.listdir(OldFolderPATH):
            if '.mp3' in song:
                audio = EasyID3(f"{OldFolderPATH}/{song}")
                audio['album'] = f"{AlbumName}"
                audio['albumartist'] = f"{AlbumName}"
                audio.save()

                shutil.move(f"{OldFolderPATH}/{song}", f"{NewFolderPATH}/{song}")
    except Exception as err:
        print(f"ERROR WAS : {err}")

inputQuary = ["https://www.youtube.com/watch?v=QalWKRmjHJA", "https://www.youtube.com/watch?v=i8wghCdMncU", "https://www.youtube.com/watch?v=3MjBlSnX51M", "https://www.youtube.com/watch?v=tm7Xf9818FM", "https://www.youtube.com/watch?v=RQmEERvqq70"]

Putbackthismusic = []

async def Worker(i):
    await asyncio.gather(
        asyncio.to_thread(YoutubeSideDownload, i),
    )

GlobalQue = ''

async def Master(Queue):
    while Queue != []:
        async with asyncio.TaskGroup() as tg:
            if len(Queue) > int(settings['Threads']):
                for x in range(int(settings['Threads'])):
                    tg.create_task(Worker(Queue.pop(0))),
            else:
                for x in range(len(Queue)):
                    tg.create_task(Worker(Queue.pop(0))),

class Navigbar(CT.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        self.currentActive = 1

        self.button1 = CT.CTkButton(self, text="New Download", command=self.NewDownload, width=200, height=50, fg_color="#1f6aa5", hover_color="#1f6aa5")
        self.button1.grid(row=0, column=0, padx=0)
        self.button2 = CT.CTkButton(self, text="Update Album", command=self.UpdateAlbums, width=200, height=50, fg_color="transparent", hover_color="#144870")
        self.button2.grid(row=0, column=1, padx=20)
        self.button3 = CT.CTkButton(self, text="Settings", command=self.Setting, width=200, height=50, fg_color="transparent", hover_color="#144870")
        self.button3.grid(row=0, column=2, padx=0)

        self.version = CT.CTkLabel(self, width=200, height=50, text=f"Version: {version}")
        self.version.grid(row=0, column=3, padx=20)

    def NewDownload(self):
        if self.currentActive != 1:
            self.currentActive = 1

            self.button1.configure(fg_color="#1f6aa5")
            self.button1.configure(hover_color="#1f6aa5")

            self.button2.configure(fg_color="transparent")
            self.button2.configure(hover_color="#144870")

            self.button3.configure(fg_color="transparent")
            self.button3.configure(hover_color="#144870")

            self.master.DEL()
            self.master.NewDownload()

    def UpdateAlbums(self):
        if self.currentActive != 2:
            self.currentActive = 2

            self.button2.configure(fg_color="#1f6aa5")
            self.button2.configure(hover_color="#1f6aa5")

            self.button1.configure(fg_color="transparent")
            self.button1.configure(hover_color="#144870")

            self.button3.configure(fg_color="transparent")
            self.button3.configure(hover_color="#144870")

            self.master.DEL()
            self.master.UpdateAlbums()
    
    def Setting(self):
        if self.currentActive != 3:
            self.currentActive = 3

            self.button3.configure(fg_color="#1f6aa5")
            self.button3.configure(hover_color="#1f6aa5")

            self.button2.configure(fg_color="transparent")
            self.button2.configure(hover_color="#144870")

            self.button1.configure(fg_color="transparent")
            self.button1.configure(hover_color="#144870")

            self.master.DEL()
            self.master.Setting()

class Frame1LeftSide(CT.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color = "transparent")

        self.label = CT.CTkLabel(master=self, text="Youtube/Spotify links")
        self.label.pack(anchor="w", padx=10)
        self.textbox = CT.CTkTextbox(master=self, width=400, height=400, corner_radius=0)
        self.textbox.pack()

class Frame1RightSide(CT.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color = "transparent")

        self.Albumlabel = CT.CTkLabel(master=self, text="Album name:")
        self.Albumtext = CT.CTkEntry(master=self, width=400, height=50, corner_radius=0)
        self.Albumlabel.pack(anchor="e", padx=40)
        self.Albumtext.pack()

        self.pad = CT.CTkLabel(master=self, text="")
        self.pad.pack(pady=20)

        self.Dirlabel = CT.CTkLabel(master=self, text="Download directory (W.I.P):")
        self.Dirtext = CT.CTkEntry(master=self, width=400, height=50, corner_radius=0)
        self.Dirlabel.pack(anchor="e", padx=40)
        self.Dirtext.pack()

        self.pad = CT.CTkLabel(master=self, text="")
        self.pad.pack(pady=20, padx=450)

        self.button = CT.CTkButton(self, text="Save", command=self.savefile, width=150, height=50)
        self.button.pack(padx=20, pady=20, anchor="e")

    def savefile(self):
        self.master.master.SaveAlbum()
        self.button.configure(text="Sucessfully Saved!", fg_color= "#78c396", hover_color="#78c396")

class Frame1(CT.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left = Frame1LeftSide(master=self)
        self.left.grid(row=0, column=0, padx=10, pady=10)

        self.right = Frame1RightSide(master=self)
        self.right.grid(row=0, column=1, padx=10, pady=10)

class SingleBar(CT.CTkFrame):
    def __init__(self, master, dir, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.dir = dir
        self.Info = LoadJson("/Saved/" + dir)
        self.Name = self.Info['Name']

        if len(self.Name) > 80:
            self.Name = self.Name[:80]

        self.Name = "{0:80}".format(self.Name)

        self.DeleteButton = CT.CTkButton(self, text="X", width=20, height=20, fg_color="#c42b1c", hover_color="#911f14", command=self.Delete)
        self.DeleteButton.grid(row=0, column=0, padx=0, sticky='w')

        self.NameLabel = CT.CTkLabel(self, text=self.Name,width=280,anchor='w')
        self.NameLabel.grid(row=0, column=1, padx=20)
        
        self.Update = CT.CTkButton(self, text="Update", command=self.Download)
        self.Update.grid(row=0, column=2, padx=0, sticky='e')

    def Download(self):
        CurrentDownloading['Name'] = self.Info['Name']
        CurrentDownloading['Dir'] = self.Info['Dir']
        CurrentDownloading['Links'] = self.Info['Links'].split('\n')

        self.master.master.master.master.destroy()

        global willDownload
        willDownload = True

    def Delete(self):
        os.remove(CMDpath+"/bin/Saved/" + self.dir)
        self.NameLabel.configure(text="DELETED")
        self.destroy()


class Frame2(CT.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        i = 0
        for x in os.listdir(CMDpath + "/bin/Saved"):
            self.label = SingleBar(master=self, dir=x)
            self.label.grid(row=i, column=0, padx=5, pady=10, sticky='w')
            i += 1

class Frame3(CT.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(3, weight=1) 
        self.grid_columnconfigure(3, weight=1)

        self.ComboBoxlabel1 = CT.CTkLabel(master=self, text="Language (W.I.P)")
        self.ComboBox1 = CT.CTkComboBox(master=self, values=["(W.I.P)"])
        self.ComboBox1.set(str(settings['Language']))
        self.ComboBox1.set("(W.I.P)") # DELETE WHEN WORKING
        self.ComboBoxlabel1.grid(row=0, column=1, padx=10, pady=20)
        self.ComboBox1.grid(row=0, column=0, padx=10)

        self.ComboBoxlabel2 = CT.CTkLabel(master=self, text="How many threads should program use:")
        self.ComboBox2 = CT.CTkComboBox(master=self, values=["1", '2', '3', '4', '6', '8', '10', '12'])
        self.ComboBox2.set(int(settings['Threads']))
        self.ComboBoxlabel2.grid(row=1, column=1, padx=10, pady=20)
        self.ComboBox2.grid(row=1, column=0, padx=10)

        
        self.Entrylabel3 = CT.CTkLabel(master=self, text="Client_id_spotify")
        self.Entry3 = CT.CTkEntry(master=self, width=200, placeholder_text=settings['Client_id_spotify'])
        self.Entrylabel3.grid(row=2, column=1, padx=10, pady=20)
        self.Entry3.grid(row=2, column=0, padx=20)

        self.Entrylabel4 = CT.CTkLabel(master=self, text="Client_secret_spotify")
        self.Entry4 = CT.CTkEntry(master=self, width=200, placeholder_text=settings['Client_secret_spotify'])
        self.Entrylabel4.grid(row=3, column=1, padx=10, pady=20)
        self.Entry4.grid(row=3, column=0, padx=20)

class FrontEnd(CT.CTk):
    def __init__(self):
        super().__init__()

        self.title("Darg Music Downloader")
        self.geometry("900x700")
        CT.set_appearance_mode("dark")

        self.Navigbar = Navigbar(master=self)
        self.Navigbar.pack(pady=10)

        self.NewDownload()
    
    def NewDownload(self):
        self.Frame1 = Frame1(master=self)
        self.Frame1.pack(padx=20, pady=20)

        self.button1 = CT.CTkButton(self, text="Download", command=self.Download, width=300, height=75)
        self.button1.pack(padx=20, pady=20)
    
    def UpdateAlbums(self):
        self.Frame2 = Frame2(master=self, width=500, height=500)
        self.Frame2.pack(padx=20, pady=20)
    
    def Setting(self):
        self.Frame3 = Frame3(master=self)
        self.Frame3.pack(padx=20, pady=20)

        self.button3 = CT.CTkButton(self, text="Save", command=self.SaveSettings, width=300, height=75)
        self.button3.pack(padx=20, pady=20)


    def DEL(self):
        lists = self.pack_slaves()
        for x in lists:
            if x != self.Navigbar:
                x.destroy()

    def SaveSettings(self):
        settings['Language'] = self.Frame3.ComboBox1.get()
        settings['Threads'] = self.Frame3.ComboBox2.get()
        if self.Frame3.Entry3.get() != '':
            settings['Client_id_spotify'] = self.Frame3.Entry3.get()
        if self.Frame3.Entry4.get() != '':
            settings['Client_secret_spotify'] = self.Frame3.Entry4.get()
        

        SaveJson(settings, 'setting.json')
        self.button3.configure(text="Sucessfully Saved!", fg_color= "#78c396", hover_color="#78c396")

    def SaveAlbum(self):
        JsonList = {
            'Name': self.Frame1.right.Albumtext.get(),
            'Dir': self.Frame1.right.Dirtext.get(),
            'Links': self.Frame1.left.textbox.get("1.0", 'end-1c'),
        }
        SaveJson(JsonList, f'Saved/{JsonList['Name']}.json')

    def Download(self):
        CurrentDownloading['Name'] = self.Frame1.right.Albumtext.get()
        CurrentDownloading['Dir'] = self.Frame1.right.Dirtext.get()
        CurrentDownloading['Links'] = self.Frame1.left.textbox.get("1.0", 'end-1c'),

        self.destroy()

        global willDownload
        willDownload = True

class Progress(CT.CTk):
    def __init__(self):
        super().__init__()

        CT.set_appearance_mode("dark")
        self.geometry("900x300")

        self.pad = CT.CTkLabel(master=self, text='')
        self.pad.pack(pady=40)

        self.Label = CT.CTkLabel(master=self, text='Downloading..."')
        self.Label.pack(pady=0)

        self.ProgressBar = CT.CTkProgressBar(master=self, width=810, height=20)
        self.ProgressBar.set(0)
        self.ProgressBar.pack()

        self.Loop()

    def Loop(self):
        global GlobalQue
        while GlobalQue != False:
            print('1')
            time.sleep(1)

class Finished(CT.CTk):
    def __init__(self):
        super().__init__()

        CT.set_appearance_mode("dark")
        self.geometry("900x300")

        self.Label = CT.CTkLabel(master=self, text='FINISHED')
        self.Label.pack(pady=80)

        self.button = CT.CTkButton(master=self, text='Close', command=self.destroy, width=300, height=75)
        self.button.pack()


if __name__ == "__main__":
    # MoveMp3Files(CMDpath, CMDpath + f"/test", "test")
    settings = LoadJson('setting.json')

    app = FrontEnd()
    try:
        app.mainloop()
    except:
        print("Exited mainloop")

    if willDownload:
        SpotifySongs = []
        YoutubeSongs = []
        DownloadingUrls = ''
        
        for x in CurrentDownloading["Links"]:
            DownloadingUrls += x + "\n"

        DownloadingUrls = DownloadingUrls.split('\n')
        print(DownloadingUrls)
        for x in DownloadingUrls:
            if 'https' in x:
                if 'spotify' in x:
                    y = x.replace('\n', '')
                    SpotifySongs.append(y)
                else:
                    y = x.replace('\n', '')
                    YoutubeSongs.append(y)
            else:
                y = x.replace('\n', '')

        for x in YoutubeSongs:
            if "list=" in x:
                YoutubeSongs.remove(x)

                try:
                    newsongs = ExtractYoutube(x)
                except Exception as err:
                    print(f"ERROR yotube fkced:{err}")
                    newsongs = []

                for y in newsongs:
                    YoutubeSongs.append(y)

        print(YoutubeSongs)
        if YoutubeSongs != []:
            asyncio.run(Master(YoutubeSongs))

        if SpotifySongs != []:
            SpotifySideDownload(SpotifySongs)

        if not os.path.exists(CMDpath + f"/{CurrentDownloading['Name']}"):
            os.mkdir(CMDpath + f"/{CurrentDownloading['Name']}")

        MoveMp3Files(CMDpath, CMDpath + f"/{CurrentDownloading['Name']}", f"{CurrentDownloading['Name']}")

        app = Finished()
        try:
            app.mainloop()
        except:
            print("Exited mainloop")