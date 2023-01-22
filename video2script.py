# pip install git+https://github.com/openai/whisper.git

import os
import glob
import whisper
import json


def split_video(vid, language='English', output="script.json", model="base"):
   language = language 
   translate = False 

   model = whisper.load_model(model)
   result = model.transcribe(vid)
   with open(output, "w") as outfile:
      json.dump(result, outfile, indent = 4) 