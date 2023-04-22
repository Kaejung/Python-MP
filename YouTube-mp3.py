from pytube import YouTube
from moviepy.editor import *
import os

def convert_to_mp3(link):
    # Chemin du dossier "Music" de Windows
    music_folder = os.path.join(os.path.expanduser("~"), "Music")

    # Télécharge la vidéo
    video = YouTube(link).streams.first().download()

    # Convertissement mp4 -> mp3 avec bitrate de 320 kbps
    mp4_file = VideoFileClip(video)
    mp3_file = mp4_file.audio.write_audiofile(os.path.join(music_folder, os.path.splitext(os.path.basename(video))[0] + ".mp3"), bitrate="320k", codec="libmp3lame")

    # Supprime mp4
    mp4_file.close()
    os.remove(video)
    print("Conversion complete!")

if __name__ == '__main__':
    link = input("Enter YouTube video link: ")
    convert_to_mp3(link)
