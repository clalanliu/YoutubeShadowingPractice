# Shadowing Practice Using Python
**Make your own VoiceTube.**
[Demo Video](https://www.youtube.com/watch?v=CEIoTZkU71c)

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python main.py [-url YOUTUBE_URL] [--pause N] [--force]
```
`--url`: Specify Youtube link. It is required for the first time use.

`--pause`: Manually set pause duration. If not set, It will equal the original sentence duration.

`--force`: Re-processing video

`--model`: Choose Whisper model size: tiny | base | small | medium | large

`--word`: At least # words in a segment. Default 5.