from get_video_from_yt import donwload
from mp4_to_mp3 import convert_video_to_audio_ffmpeg
from video2script import split_video
import sys
import os
from player_segbyseg import play
import argparse

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", '-u', default=None)
    parser.add_argument('--force', '-f', help="Force downlading", action="store_true")
    parser.add_argument('--pause', '-p', help="If set, pause # second after each segment", default=0, type=float)
    parser.add_argument('--model', '-m', help="Model Size [tiny|base|small|medium|large]", default="base")
    parser.add_argument('--words', '-w', help="Pause after at least # words", default=5, type=int)
    parser.add_argument('--speed', '-s', help="Adjust speed to #-X. Default 1-X. If negative, represents for #-words per min.", default=1.0, type=float)
    return parser

if __name__ == "__main__":
    args = get_parser().parse_args()

    if args.url != None:
        if not os.path.exists("script.json") or args.force:
            print("Downloading ...")
            donwload(args.url)
            print("Converting ...")
            convert_video_to_audio_ffmpeg('test.mp4')
            print("Generating Scripts ...")
            split_video('test.mp3', model=args.model)

    if os.path.exists("script.json"):
        if args.pause > 0:
            print(f"Playing with pause={args.pause} seconds")
            
        play('test.mp3', 'script.json', stop=args.pause, n_words=args.words, speed=args.speed)
