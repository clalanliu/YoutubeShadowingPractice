 
import json
import pyaudio
from pydub import AudioSegment
import time
import os
import winsound
import numpy as np

beep_frequency = 2500  # Set Frequency To 2500 Hertz
beep_duration = 200  # Set Duration To 1000 ms == 1 second

# ref: https://stackoverflow.com/questions/51434897/how-to-change-audio-playback-speed-using-pydub
def change_audioseg_tempo(audiosegment, tempo_ratio):
    import pyrubberband as pyrb
    os.environ["PATH"] += os.pathsep + "rubberband-3.1.2-gpl-executable-windows"

    y = np.array(audiosegment.get_array_of_samples())
    if audiosegment.channels == 2:
        y = y.reshape((-1, 2))

    sample_rate = audiosegment.frame_rate

    y_fast = pyrb.time_stretch(y, sample_rate, tempo_ratio)

    channels = 2 if (y_fast.ndim == 2 and y_fast.shape[1] == 2) else 1
    y = np.int16(y_fast * 2 ** 15)

    new_seg = AudioSegment(y.tobytes(), frame_rate=sample_rate, sample_width=2, channels=channels)

    return new_seg


def play(mp3_path="test.mp3", script_path='script.json', stop=0, n_words=10, speed=1.0):
    

    # Opening JSON file
    with open(script_path) as f:
        data = json.load(f)

    # Assign a mp3 source file to the PyDub Audiosegment
    mp3_full = AudioSegment.from_mp3(mp3_path)
    
    # Adjust speed
    word_per_min = len(data['text'].split()) / (mp3_full.duration_seconds/60) 
    print(f"Original speed: {word_per_min:.04}/min")
    if speed > 0 and not np.isclose(speed, 1.0):
        print(f"Adjusting Speed to {speed*word_per_min:.04}/min. ({speed}x)")
    if speed < 0: # Use negative to represent num-words/min
        print(f"Adjusting Speed to {-speed:.04}/min. ({-speed / word_per_min :.04}x)")
        speed = -speed / word_per_min 
    # Assign the PyAudio player
    player = pyaudio.PyAudio()

    # Concate seg if word num < words
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

    # play seg
    for seg in segs:
        start = seg['start']*1000
        end = seg['end']*1000

        # play data
        mp3 = mp3_full[int(start):int(end)]
        
        if not np.isclose(speed, 1.0, 0.05):
            if speed > 1.0:
                mp3 = mp3.speedup(speed) # https://github.com/jiaaro/pydub/blob/72b474e0f2e48d37bbe9b8a36c4a055157e53c6b/pydub/effects.py
            else:
                mp3 = change_audioseg_tempo(mp3, speed)
                

        print(f"[{time.strftime('%H:%M:%S', time.gmtime(seg['start']))}:{time.strftime('%H:%M:%S', time.gmtime(seg['end']))}]{seg['text']}")
        stream = player.open(format = player.get_format_from_width(mp3.sample_width),
            channels = mp3.channels,
            rate = mp3.frame_rate,
            output = True)

        data = mp3.raw_data

        while data:
            stream.write(data)
            data=0

        stream.close()
        

        # Beep and play
        if stop == 0:
            winsound.Beep(beep_frequency, beep_duration)

        if stop != 0:
            time.sleep(stop)
        else:
            time.sleep((end-start)/1000.0)


    player.terminate()