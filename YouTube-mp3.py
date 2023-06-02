import os
import subprocess
import sys

# List of required packages
REQUIRED_PACKAGES = ['pytube']

# Check and install missing packages
for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check for package updates
for package in REQUIRED_PACKAGES:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    except subprocess.CalledProcessError:
        pass

from pytube import YouTube
from moviepy.editor import *
import threading
import tkinter as tk
from tkinter import ttk, messagebox

def download_video():
    link = entry_link.get()
    music_folder = os.path.join(os.path.expanduser("~"), "Music")

    def download():
        try:
            yt = YouTube(link)
            stream = yt.streams.get_highest_resolution()
            video_path = stream.download(output_path=music_folder)

            mp4_file = VideoFileClip(video_path)
            mp3_file = mp4_file.audio.write_audiofile(
                os.path.join(music_folder, os.path.splitext(os.path.basename(video_path))[0] + ".mp3"),
                bitrate="320k", codec="libmp3lame"
            )

            mp4_file.close()
            os.remove(video_path)

            messagebox.showinfo("Conversion Successful", "Video converted to MP3 successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Reset the progress bar
            progress_bar.stop()
            progress_bar['value'] = 0

            answer = messagebox.askyesno("Download Another Video", "Do you want to download and convert another video?")
            if answer:
                entry_link.delete(0, tk.END)  # Clear the previous link
            else:
                os._exit(0)  # Terminate the program

    # Start the download in a separate thread
    download_thread = threading.Thread(target=download)
    download_thread.start()

    # Show the progress bar
    progress_bar.start()


# Create the GUI window
window = tk.Tk()
window.title("YouTube Video to MP3 Converter")
window.configure(bg='black')

# Calculate the center position of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 400
window_height = 250
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and position the video link label
label_link = tk.Label(window, text="Enter YouTube Video Link:", bg='black', fg='white')
label_link.pack(pady=10)

# Create a themed style for the input field
style = ttk.Style()
style.configure('TEntry', background='black', foreground='black', fieldbackground='black', borderwidth=0,
                relief='solid', padding=5)

# Create and position the rounded input field
entry_link = ttk.Entry(window, width=50, style='TEntry')
entry_link.configure(foreground='black')  # Set text color to black
entry_link.pack()

# Create and position the download button with rounded corners
button_download = tk.Button(window, text="Download and Convert", command=download_video, bg='gray', fg='white',
                            relief='solid', bd=0, padx=10, pady=5)
button_download.configure(borderwidth=0, highlightthickness=0)
button_download.pack(pady=10)

# Create and position the progress bar
progress_bar = ttk.Progressbar(window, mode='indeterminate')
progress_bar.pack(pady=10)

# Run the GUI window
window.mainloop()