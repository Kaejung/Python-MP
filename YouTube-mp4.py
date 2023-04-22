import os
from pytube import YouTube

if __name__ == '__main__':
    link = input("Enter YouTube video link: ")

# Chemin du dossier "Videos" de Windows
video_folder = os.path.join(os.path.expanduser("~"), "Videos")

# Télécharger la vidéo dans le dossier "Videos" de Windows
yt = YouTube(link)
stream = yt.streams.get_highest_resolution()
stream.download(output_path=video_folder)

