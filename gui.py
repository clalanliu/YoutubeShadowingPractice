import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from get_video_from_yt import download
from mp4_to_mp3 import convert_video_to_audio_ffmpeg
from video2script import split_video
import os
from player_segbyseg import play
import argparse

def download_video():
    url = url_entry.get()
    force_download = force_var.get()

    if (not os.path.exists("script.json") or force_download) and not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    try:
        if not os.path.exists("script.json") or force_download:
            download(url)
            messagebox.showinfo("Success", "Video downloaded successfully.")

            # Convert video to audio and generate scripts
            convert_video_to_audio_ffmpeg('test.mp4')
            split_video('test.mp3', model=model_var.get(), prune=True)

        if pause_var.get() > 0:
            messagebox.showinfo("Info", f"Playing with pause={pause_var.get()} seconds")

        play('test.mp3', 'script.json', stop=pause_var.get(), n_words=words_var.get(), speed=speed_var.get())

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Script Player")

# Create and configure frame
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

# URL Entry
url_label = tk.Label(frame, text="YouTube URL:")
url_label.pack()
url_entry = tk.Entry(frame, width=40)
url_entry.pack()

# Force Download Checkbox
force_var = tk.BooleanVar()
force_checkbox = tk.Checkbutton(frame, text="Force Download", variable=force_var)
force_checkbox.pack()

# Model Size Radiobuttons
model_label = tk.Label(frame, text="Model Size:")
model_label.pack()
model_var = tk.StringVar()
model_var.set("base")
model_options = ["tiny", "base", "small", "medium", "large"]
for model_option in model_options:
    model_radio = tk.Radiobutton(frame, text=model_option, variable=model_var, value=model_option)
    model_radio.pack()

# Pause Entry
pause_label = tk.Label(frame, text="Pause after (seconds):")
pause_label.pack()
pause_var = tk.DoubleVar(value=0.0)
pause_entry = tk.Entry(frame, width=10, textvariable=pause_var)
pause_entry.pack()

# Words Entry
words_label = tk.Label(frame, text="Pause after at least # words:")
words_label.pack()
words_var = tk.IntVar(value=5)
words_entry = tk.Entry(frame, width=10, textvariable=words_var)
words_entry.pack()

# Speed Entry
speed_label = tk.Label(frame, text="Adjust speed to (1-X or words per min):")
speed_label.pack()
speed_var = tk.DoubleVar(value=1.0)
speed_entry = tk.Entry(frame, width=10, textvariable=speed_var)
speed_entry.pack()

# Download Button
download_button = tk.Button(frame, text="Download and Play", command=download_video)
download_button.pack()

# Run the GUI
root.mainloop()