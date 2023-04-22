import os
from pytube import YouTube
from moviepy.editor import *

#Coller le lien YouTube
if __name__ == '__main__':
    link = input("Enter YouTube video link: ")

#Chemin du dossier "Music" de Windows
music_folder = os.path.join(os.path.expanduser("~"), "Music")

#Télécharger la vidéo
yt = YouTube(link)
stream = yt.streams.get_highest_resolution()
video_path = stream.download(output_path=music_folder)

#Convertir la vidéo en mp3 avec une qualité audio de 320 kbps
mp4_file = VideoFileClip(video_path)
mp3_file = mp4_file.audio.write_audiofile(os.path.join(music_folder, os.path.splitext(os.path.basename(video_path))[0] + ".mp3"), bitrate="320k", codec="libmp3lame")

#Supprimer le fichier vidéo
mp4_file.close()
os.remove(video_path)
