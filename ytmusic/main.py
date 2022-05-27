from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
import time

# Declaring the main class object
api = YTMusic("headers_auth.json")


#search_results = api.search(query="Queen - God Save The Queen  audio", filter="songs", limit=1)

#artist_info = api.get_artist(channelId='UCUDVBtnOQi4c7E8jebpjc9Q')

#print(search_results)


# REMINDER: best format -> 'm4a/bestaudio/best'
#           best way to convert -> 'mp3'

start = time.time()

url = ['https://www.youtube.com/watch?v=1wYNFfgrXTI', 'https://www.youtube.com/watch?v=S9bCLPwzSC0', 'https://www.youtube.com/watch?v=j5-yKhDd64s', 'https://www.youtube.com/watch?v=Pi3_Zs-oRUo', 'https://www.youtube.com/watch?v=eVTXPUF4Oz4']

u = 'https://www.youtube.com/watch?v=W4Uzgxw_mT4'
ydl_opts = {'format': 'm4a/bestaudio/best',
            'quiet': True}
'''
ydl_opts = {'format': 'm4a/bestaudio/best',
            'quiet': True',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'}]
            }
'''

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(u)

print(time.time() - start)
