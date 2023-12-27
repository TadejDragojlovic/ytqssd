import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import os

import time

from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL

# TODO:
'''
  * Benchmark?
  * Figure out how would the YTMusic api authorization work on complete website.
  * Multithreading?
'''

API = YTMusic()

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

def gatherLinks(songs: list):
    '''
    * PARAMETERS:
    - song_list [list]: list containing the song names

    * DESCRIPTION:
    Constructs youtube links for all inputed songs. (Finds their videoIds)

    * RETURN:
    -> Returns a list of links for each song. list
    '''

    #start = time.time()
    base_url = 'https://www.youtube.com/watch?v='

    results = []
    print("searching...")
    for song in songs:
        search_results = API.search(query=song, limit=20)

        top_result = _skipGarbage(search_results)
        if top_result != -1:
            results.append(f"{base_url}{search_results[top_result]['videoId']}")
        else:
            print(f"Nothing was found for a given keyword. ({song})")

    #print("Finished `_testYTMusic()` in : %f" % (time.time() - start))
    return results


# Doc: "https://ytmusicapi.readthedocs.io/en/stable/reference.html#ytmusicapi.YTMusic.search"
def _search(keyword: str):
    base_url = 'https://www.youtube.com/watch?v='

    search_results = API.search(query=keyword, filter="songs", limit=5)
    # top_results = _skipGarbage(search_results) # REMINDER: this is useful for console app

    return search_results

# Helper function for `getLinksYTMUSIC()`
def _skipGarbage(search_results: list):
    '''
    * PARAMETERS:
    - search_results [list]: a list containing results from `API.search()`

    * DESCRIPTION:
    Check for errors and find the first 'song' or 'video' in the provided list

    * RETURN:
    -> Returns the list of valid results, valid results are only of type `videos` or `songs`. [list]
    '''

    '''
    REMINDER: OVAKO SE RADI NA NOVOM SAJTU, A INDEX VRACA NA STARI NACIN
    valid_results = []

    for result in search_results:
        if result['resultType'] == 'song' or result['resultType'] == 'video':
            valid_results.append(result)

    return valid_results
    '''

    for result in search_results:
        if result['resultType'] == 'song' or result['resultType'] == 'video':
            return search_results.index(result)

    return -1


def downloadSongs(song_links: list):
    # REMINDER: Only 'm4a' FORMAT SO FAR

    start = time.time()
    default_path = str(os.getcwd())+'/songs'

    ydl_opts = {'format': 'm4a',
                'quiet': True,
                'paths': {'home': default_path},
                }

    print("Downloading...")
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(song_links)

    print("Download finished.")


if __name__ == '__main__':
    start = time.time()

    print("aaaaaa")

    """
    song_list = _readFile('maki/maki-pop.txt')
    print("Succesfully imported.")

    # print("Songs: ", song_list)

    song_links = getLinksYTMUSIC(song_list)

    print("Links: ", song_links)

    _downloadSongs(song_links, format='mp4')

    """

    print("Finished `main()` in : %f" % (time.time() - start))
