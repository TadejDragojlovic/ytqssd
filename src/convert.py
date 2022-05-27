from moviepy.editor import *
import os

def get_songs(song_folder_path:str):
    songs = os.listdir(song_folder_path)

    return songs

def convert_to_mp3(raw_extension:str, songs: list,song_folder_path:str, converted_folder_path:str):

    for song in songs:
        raw_file = song_folder_path + song
        mp3_file = converted_folder_path + song.replace(raw_extension, "mp3")

        audioclip = AudioFileClip(raw_file)
        audioclip.write_audiofile(filename=mp3_file)

        audioclip.close()

    print("Konvertovano u mp3.")
