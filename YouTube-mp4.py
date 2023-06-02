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
import threading
import tkinter as tk
from tkinter import ttk, messagebox

def download_video():
    link = entry_link.get()

    def download():
        try:
            yt = YouTube(link)
            stream = yt.streams.get_lowest_resolution()
            if stream:
                stream.download()
                messagebox.showinfo("Download Successful", "Video downloaded successfully!")
            else:
                messagebox.showerror("Error", "Unable to retrieve video stream.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Reset the progress bar
            progress_bar.stop()
            progress_bar['value'] = 0

            answer = messagebox.askyesno("Download Another Video", "Do you want to download another video?")
            if answer:
                entry_link.delete(0, tk.END)  # Clear the previous link
            else:
                window.quit()  # Close the application

    # Start the download in a separate thread
    download_thread = threading.Thread(target=download)
    download_thread.start()

    # Show the progress bar
    progress_bar.start()

# Create the GUI window
window = tk.Tk()
window.title("YouTube Video Downloader")
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
style.configure('TEntry', background='black', foreground='black', fieldbackground='black', borderwidth=0, relief='solid', padding=5)

# Create and position the rounded input field
entry_link = ttk.Entry(window, width=50, style='TEntry')
entry_link.pack()

# Create and position the download button with rounded corners
button_download = tk.Button(window, text="Download", command=download_video, bg='gray', fg='white', relief='solid', bd=0, padx=10, pady=5)
button_download.configure(borderwidth=0, highlightthickness=0)
button_download.pack(pady=10)

# Create and position the progress bar
progress_bar = ttk.Progressbar(window, mode='determinate', maximum=100, style='TProgressbar')
progress_bar.pack(pady=10)

# Configure the style for the progress bar
style.configure('TProgressbar', background='black', troughcolor='black', bordercolor='white')

# Run the GUI window
window.mainloop()
