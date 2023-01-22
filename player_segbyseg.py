 
import json
import pyaudio
from pydub import AudioSegment
import time
import os
import winsound

def play(mp3_path="test.mp3", script_path='script.json', stop=0, n_words=10):
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 200  # Set Duration To 1000 ms == 1 second

    # Assign a mp3 source file to the PyDub Audiosegment
    mp3_full = AudioSegment.from_mp3(mp3_path)

    # Assign the PyAudio player
    player = pyaudio.PyAudio()

    # Create the stream from the chosen mp3 file

    # Opening JSON file
    with open(script_path) as f:
        data = json.load(f)

    # Concate if word num < words
    segs = []
    word_num = 0
    for seg in data['segments']:
        if word_num==0:
            segs.append({
                'start': seg['start'],
                'end': seg['end'],
                'text': seg['text']
            })
            word_num += len(seg['text'].split())
        else:
            segs[-1]['end'] = seg['end']
            segs[-1]['text'] += seg['text']
            word_num += len(seg['text'].split())

        if word_num >= n_words:
            word_num = 0


    for seg in segs:
        start = seg['start']*1000
        end = seg['end']*1000

        mp3 = mp3_full[int(start):int(end)]
        print(seg['text'])
        stream = player.open(format = player.get_format_from_width(mp3.sample_width),
            channels = mp3.channels,
            rate = mp3.frame_rate,
            output = True)

        data = mp3.raw_data

        while data:
            stream.write(data)
            data=0

        stream.close()
        
        if stop == 0:
            winsound.Beep(frequency, duration)

        if stop != 0:
            time.sleep(stop)
        else:
            time.sleep((end-start)/1000.0)


    player.terminate()