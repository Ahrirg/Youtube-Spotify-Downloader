# import spotdl
import os, shutil
import yt_dlp
from spotdl import Spotdl
from mutagen.easyid3 import EasyID3

Client_id_spotify = "47eb5313f7bf40339fc5cfb2c9186d13"
Client_secret_spotify = "6e4a2415ddd542d280e8250063553e27"


def SpotifySideDownload(List):
    print('Starting Spotify download')
    Sdl = Spotdl(client_id=Client_id_spotify, client_secret=Client_secret_spotify, no_cache=True)

    song_objs = Sdl.search(List)

    for x in song_objs:
        print(x.name, end=", ")

    Sdl.download_songs(song_objs)
    print("Spotify download has finished")

def YoutubeSideDownload(List):
    ytdlp_opts = {
        'format': 'bestaudio/best',
        'skip-unavailable-fragments': True,
        'addmetadata': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ytdlp_opts) as ytdl:
        ytdl.download(List)
    print("Youtube download has finished")



print("""\n\n
      ########       ###     #########    ########            ###    ###                ########    ###  
     ###    ###   ### ###   ###     ### ###    ###          #####  #####               ###    ###  ###   
    ###    ###  ###   ###  ###     ### ###                ###  #####  ###             ###    ###  ###    
   ###    ### ########### #########   ###                ###   ###   ###   #######   ###    ###  ###     
  ###    ### ###     ### ###     ### ###   #####        ###         ###             ###    ###  ###      
 ###    ### ###     ### ###     ### ###     ###        ###         ###             ###    ###  ###       
########   ###     ### ###     ###  ##########        ###         ###             ########    ########## \n\n""")

PathofCode = os.getcwd()

print(os.listdir(PathofCode))

FolderN = input('Custom Album name: ')

if FolderN == "":
    FolderN = "Unnamed"

FolderPath = os.path.join(PathofCode, FolderN)

try:
    os.mkdir(FolderPath)
except:
    print('\n//---//---//---//\nError has been cought\n//---//---//---//\n')
    shutil.rmtree(FolderPath)
    os.mkdir(FolderPath)

# f = open('List.txt', "a")
# f.close()


fowards = False
while fowards == False:
    inputQuary = input('(If blank will try use "List.txt" and download all of the music from that) -=- Music name or url: ')

    if inputQuary == "":
        f = open('List.txt', "r")
        data = f.readlines()
        f.close()
        if data != []:
            print(data)
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

SpotifySideDownload(SpotifySongs)
YoutubeSideDownload(YoutubeSongs)

for song in os.listdir(PathofCode):
    if '.mp3' in song:
        audio = EasyID3(f"{song}")
        audio['album'] = f"{FolderN}"
        audio['albumartist'] = f"{FolderN}"
        audio.save()

        print(audio)

        shutil.move(f"{PathofCode}/{song}", f"{PathofCode}/{FolderN}/{song}")
        