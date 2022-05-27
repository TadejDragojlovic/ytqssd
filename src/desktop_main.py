import urllib.request
from bs4 import BeautifulSoup
import pytube
import re
import os
import sys
import ffmpeg
import convert

import time

#TODO: dodaj obavestenja da se downloaduju pesme
#TODO: mozda neki komentar i ocisti kod

def fileHandling(filename: str):
    with open(filename, "r") as f:
        s = f.read()

    songs = s.split('\n')

    # Ovo je za brisanje svih praznih linija (invalid song input)
    if "" in songs: songs.remove("")

    return songs

def formatQuery(songs: list): # adds '+' inbetween words so no problem with requesting the url later
    for i in range(len(songs)):
        songs[i] = "+".join(songs[i].split())

def gatherSongLinks(songs: list):
    song_links = []
    base_yt_link = 'https://www.youtube.com/watch?v='


    for song in songs:
        url = f'https://www.youtube.com/results?search_query={song}'
        # print(url)
        print(f"Pretrazivanje: {song}")
        response = urllib.request.urlopen(url).read().decode()
        soup = BeautifulSoup(response, "lxml")

        song_links.append(base_yt_link + re.findall(r"watch\?v=(\S{11})", str(soup))[0])

    return song_links

def createNewDir(name:str):
    try:
        os.mkdir(path=f"./{name}")
    except FileExistsError as e:
        print("GRESKA: Vec postoji folder sa datim imenom.")
        sys.exit(1)

def _ffmpegTest():
    s = time.time()


    ''' 1
    yt = pytube.YouTube("https://www.youtube.com/watch?v=1wYNFfgrXTI")
    y = yt.streams.filter(only_audio=True).first()
    y.download()
    os.system("ffmpeg -i 'Eminem - When Im Gone (Official Music Video).mp4' 'converted.mp3'")
    '''

    yt = pytube.YouTube("https://www.youtube.com/watch?v=W4Uzgxw_mT4")
    y = yt.streams.filter(only_audio=True).first()
    y.download()
    #convert.convert_to_mp3(raw_extension= "mp4", songs=[], song_folder_path='',
    #                       converted_folder_path='')

    # TODO: ISTRAZI KAKO REAGUJE PROGRAM AKO IMPORTUJEM yt-dlp I DIREKTNO JE
    # UPRAZNJAVAM
    #url = ['https://www.youtube.com/watch?v=1wYNFfgrXTI', 'https://www.youtube.com/watch?v=S9bCLPwzSC0', 'https://www.youtube.com/watch?v=j5-yKhDd64s', 'https://www.youtube.com/watch?v=Pi3_Zs-oRUo', 'https://www.youtube.com/watch?v=eVTXPUF4Oz4']
    #os.system(f"yt-dlp -x --audio-format mp3 {url}")

    print(time.time() - s)

def downloadSongs(song_links:list, location:str, format:str):
    '''
    Ako je izabran format 'mp3', onda moramo da skinemo video 'mp4' da bismo uspesno konvertovali u mp3
    -
    Ako je izabran format 'mp4', onda prosto mozemo da izaberemo type 'audio' i nece biti potrebno konvertovanje
    '''
    if format_option == 'mp3':
        _type = "video"
    else:
        _type = "audio"

    for link in song_links:
        yt = pytube.YouTube(link)
        y = yt.streams.filter(file_extension="mp4", type=_type).first()
        y.download(location)
        print("Skidanje muzike...")

if __name__ == '__main__':
    start=time.time()
    song_file = 'songs'

    format_option = str(input("Izaberi format: ('mp3', 'mp4')\n"))
    if format_option != 'mp3' and format_option != 'mp4':
        print("GRESKA: Pogresan format unet.")
        sys.exit(1)


    songs = fileHandling(filename='songs.txt') # Reads songs from a file
    formatQuery(songs)
    song_links = gatherSongLinks(songs)
    createNewDir(song_file)
    downloadSongs(song_links, song_file, format_option)

    #TODO: ovde napraviti ako treba konvertovanje ili ne
    if format_option == 'mp3':
        converted_path = 'converted'

        createNewDir(converted_path)

        songs = convert.get_songs(song_file)
        convert.convert_to_mp3(raw_extension='mp4', songs=songs,
        song_folder_path=song_file+'/',
        converted_folder_path=converted_path+'/')
    #_ffmpegTest()


    print("\n\nGotovo.")
    print("Finished `main()` in : %f" % (time.time() - start))
