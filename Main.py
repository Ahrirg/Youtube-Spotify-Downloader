import os, shutil
import yt_dlp
from spotdl import Spotdl
from mutagen.easyid3 import EasyID3
from tkinter import *

Client_id_spotify = ""
Client_secret_spotify = ""

PathofCode = os.path.dirname(__file__)
CMDpath = os.getcwd()

Putbackthismusic = []

print("""\n\n
      ########       ###     #########    ########            ###    ###                ########    ###  
     ###    ###   ### ###   ###     ### ###    ###          #####  #####               ###    ###  ###   
    ###    ###  ###   ###  ###     ### ###                ###  #####  ###             ###    ###  ###    
   ###    ### ########### #########   ###                ###   ###   ###   #######   ###    ###  ###     
  ###    ### ###     ### ###     ### ###   #####        ###         ###             ###    ###  ###      
 ###    ### ###     ### ###     ### ###     ###        ###         ###             ###    ###  ###       
########   ###     ### ###     ###  ##########        ###         ###             ########    ########## \n\n""")



master = Tk()
Label(master, text='List name').grid(row=0)
Label(master, text='Album name').grid(row=1)
master.title('Offbrand spotify')

e1 = Text(master)
e2 = Entry(master, width=50)


ListGuiData = ''
AlbumName = ''

def SAVETOVARIABLE():
    global ListGuiData
    global AlbumName
    
    ListGuiData = e1.get("1.0",END)
    AlbumName = e2.get()

    master.destroy()

e3 = Button(master, text='Download', width=50, command=SAVETOVARIABLE)
e1.grid(row=0, column=1, pady=5)
e2.grid(row=1, column=1, pady=7)
e3.grid(row=2, column=1, pady=7)

mainloop()


f = open(f'{PathofCode}/List.txt', "w")
f.write(ListGuiData)
f.close()

FolderN = AlbumName

if FolderN == "":
    FolderN = "Unnamed"

FolderPath = os.path.join(PathofCode, FolderN)

try:
    os.mkdir(FolderPath)
except:
    print('\n//---//---//---//\nFolder Was already made\n//---//---//---//\n')


def SpotifySideDownload(List):
    print('Starting Spotify download')
    Sdl = Spotdl(client_id=Client_id_spotify, client_secret=Client_secret_spotify, no_cache=True)

    song_objs = Sdl.search(List)

    for x in song_objs:
        # print(x.name, end=", ")
        Putbackthismusic.append(f'{x.artist} - {x.name}.mp3')
        
    Sdl.download_songs(song_objs)
    print("Spotify download has finished")

def YoutubeSideDownload(List):
    ytdlp_opts = {
        'format': 'bestaudio/best',
        'skip-unavailable-fragments': True,
        'addmetadata': True,
        'outtmpl': f'{PathofCode}/%(title)s.%(ext)s',

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
        ytdl.download(List)
    print("Youtube download has finished")



fowards = False
while fowards == False:
    inputQuary = ""

    if inputQuary == "":
        f = open(f'{PathofCode}/List.txt', "r")
        data = f.readlines()
        f.close()
        if data != []:
            # print(data)
            inputQuary = data
            fowards = True
    else:
        inputQuary = [inputQuary]
        fowards = True


SpotifySongs = []
YoutubeSongs = []
NameSongs = []

for x in inputQuary:
    if 'https' in x:
        if 'spotify' in x:
            y = x.replace('\n', '')
            SpotifySongs.append(y)
        else:
            y = x.replace('\n', '')
            YoutubeSongs.append(y)
    else:
        y = x.replace('\n', '')
        NameSongs.append(y)


# print(f'Filtered songs//\nYoutube: {YoutubeSongs}\nSpotify: {SpotifySongs}\nNameSongs: {NameSongs}')
try:
    YoutubeSideDownload(YoutubeSongs)
except Exception as err:
    print(f"ERROR WAS : {err}")

for x in Putbackthismusic:
    try: 
        shutil.move(f"{CMDpath}/{x}", f"{PathofCode}/{x}")
    except:
        print('Buvo error no wories tho')

try:
    SpotifySideDownload(SpotifySongs)
except Exception as err:
    print(f"ERROR WAS : {err}")


# print(os.listdir(PathofCode))
try:
    for song in os.listdir(PathofCode):
        # print(song)
        if '.mp3' in song:
            audio = EasyID3(f"{PathofCode}/{song}")
            audio['album'] = f"{FolderN}"
            audio['albumartist'] = f"{FolderN}"
            audio.save()

            # print(audio)

            shutil.move(f"{PathofCode}/{song}", f"{PathofCode}/{FolderN}/{song}")
except Exception as err:
    print(f"ERROR WAS : {err}")

print('-=- Press enter to Finish -=-')

masterFN = Tk()
masterFN.title('Offbrand spotify')
Label(masterFN, text='Finished').grid(row=0)
e3 = Button(masterFN, text='Done', width=50, command=masterFN.destroy)
e3.grid(row=1, column=1)
mainloop()
masterFN.destroy