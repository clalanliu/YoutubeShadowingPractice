# pip install git+https://github.com/openai/whisper.git

import os
import glob
import whisper
import json
import sys

def split_video(vid, language='English', output="script.json", model="base", prune=True):
   language = language 
   translate = False 

   model = whisper.load_model(model)
   result = model.transcribe(vid)


   if prune:
      result_concise = {
         'text-length': len(result['text'].split()),
         'segments': []
      }
      for r in result['segments']:
         result_concise['segments'].append(
            {
               "start": r["start"],
               "end": r["end"],
               "text": r["text"],
         },
         )
      result = result_concise

   with open(output, "w") as outfile:
      json.dump(result, outfile, indent = 4, ensure_ascii=False) 


if __name__ == "__main__":
   split_video(sys.argv[1], language='English', output="script.json", model="base", prune=True)