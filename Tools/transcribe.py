from pathlib import Path
import json,wave,numpy as np
from faster_whisper import WhisperModel
cache=Path.home()/'.cache/leiyu-audio-models/whisper'
model=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=6,download_root=str(cache),local_files_only=True)
for name in ['one','two']:
 with wave.open('Work/'+name+'16.wav') as w:
  audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
 segments,_=model.transcribe(audio,language='zh',word_timestamps=True,beam_size=5,condition_on_previous_text=False,vad_filter=False)
 rows=[]
 for s in segments:
  row={'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in (s.words or [])]}
  rows.append(row);print(name,json.dumps(row,ensure_ascii=False),flush=True)
 Path('Work/'+name+'-transcript.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
