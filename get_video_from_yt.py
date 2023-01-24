# python -m pip install --upgrade pytube
from pytube import YouTube
import sys

def download(url, filename="test.mp4"):
    selected_video = YouTube(url)
    audio = selected_video.streams.filter(only_audio=True, file_extension='mp4').first()
    audio.download(output_path=".", filename=filename)


if __name__ == "__main__":
    download(sys.argv[1])