import urllib.request
from bs4 import BeautifulSoup
import re
import sys

import time

from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL


# NOTE:
'''
  * No real implementation of input yet, just reading from a file for easier
  testing
'''

# TODO:
'''
  * Implement easy way to benchmark functions
  * Figure out how would the YTMusic api authorization work on complete website.
  * Multithreading (and test on the website)
  * Add function for renaming downloaded files
  * Do you remove the songs (and the list) after download process is completed on the website?
    * If so, make the function to purge all data after download process is finished
  * Check for format (mp3 or mp4) in `_downloadSongs()`
'''

def _readFile(filename: str):
    '''
    * PARAMETERS:
    - filename [str]: name of the input file (or path)

    * DESCRIPTION:
    Reads input from a given file.

    * RETURN:
    -> Returns a list of song names. [list]
    '''

    with open(filename, "r") as f:
        s = f.read()

    songs = s.split("\n")
    if "" in songs: songs.remove("") # remove empty lines

    return songs

def getLinksYTMUSIC(songs: list):
    '''
    * PARAMETERS:
    - song_list [list]: list containing the song names

    * DESCRIPTION:
    Constructs youtube links for all inputed songs. (Finds their videoIds)

    * RETURN:
    -> Returns a list of links for each song. [list]
    '''
    API = YTMusic("stuff/headers_auth.json")

    #start = time.time()

    base_url = 'https://www.youtube.com/watch?v='

    results = []
    for song in songs:
        print("searching...")
        results.append(f"{base_url}{API.search(query=song, limit=3)[0]['videoId']}")

    #print("Finished `_testYTMusic()` in : %f" % (time.time() - start))
    return results

def _downloadSongs(song_links: list, format: str):

    default_path = '/home/taduj/python/song-downloader/songs'

    ydl_opts = {'format': 'm4a/bestaudio/best',
                'quiet': True,
                'paths': {'home': default_path},
                'postprocessors': [] if format=='mp4' else \
                [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'}]
                }

    print("Downloading...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(song_links)

    print("Download finished.")


if __name__ == '__main__':
    #start = time.time()

    print("Succesfully imported.")

    #song_list = _readFile('songs.txt')

    #song_links = getLinksYTMUSIC(song_list)

    #_downloadSongs(song_links, format='mp4')

    #print("Finished `main()` in : %f" % (time.time() - start))
