# python -m pip install --upgrade pytube
from pytube import YouTube
import sys

def donwload(url, filename="test.mp4"):
    selected_video = YouTube(url)
    audio = selected_video.streams.filter(only_audio=True, file_extension='mp4').first()
    audio.download(output_path=".", filename=filename)


if __name__ == "__main__":
    donwload(sys.argv[1])