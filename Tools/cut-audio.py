from pathlib import Path
import json, wave, numpy as np
# Transcription checked against the original videos' on-screen captions.
items=[
 ('one',0,1.46,'弱者才会喝饮料。'),
 ('one',1.46,3.36,'强者会选择喝这种屌丝大水。'),
 ('one',3.36,6.71,'无论走到哪儿，把这大水往桌上一墩，能喝一整天。'),
 ('two',0,2.06,'你唯一要买的东西就是这种大水。'),
 ('two',2.06,8.48,'身边人还在炫耀咖啡奶茶，并用它们摧残自己身体的时候，咱直接把这大水往桌上一放，展示强者姿态。'),
 ('two',8.48,10.12,'给他们全部整出来，幸福者退让。'),
 ('two',10.12,12.82,'又便宜又实惠，而且一次能喝一整天。'),
 ('two',12.82,17.715,'最主要的是，无论上课还是开会，你直接把它拿着开始健身，能作为健身器材。'),
]
assets=Path('Assets/Clips');assets.mkdir(parents=True,exist_ok=True)
cache={};result=[];records=[]
for idx,(name,start,end,label) in enumerate(items,1):
 if name not in cache:
  with wave.open('Work/'+name+'44.wav','rb') as f:
   rate,channels=f.getframerate(),f.getnchannels()
   data=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,channels).astype(np.float64)/32768
   cache[name]=(rate,channels,data)
 rate,channels,data=cache[name]
 # A small overlap retains word endings at close speech boundaries; fades prevent clicks.
 a=max(0,int((start-0.03)*rate));b=min(len(data),int((end+0.03)*rate))
 x=data[a:b].copy();rms=np.sqrt(np.mean(x*x));peak=np.max(np.abs(x))
 gain=min(0.1/max(rms,1e-8),0.95/max(peak,1e-8),2.0)
 x*=gain
 fade=min(int(.005*rate),len(x)//2)
 if fade: x[:fade]*=np.linspace(0,1,fade)[:,None];x[-fade:]*=np.linspace(1,0,fade)[:,None]
 pcm=np.clip(np.rint(x*32767),-32768,32767).astype('<i2')
 filename=f'{idx:02}.wav'
 with wave.open(str(assets/filename),'wb') as out:
  out.setnchannels(channels);out.setsampwidth(2);out.setframerate(rate);out.writeframes(pcm.tobytes())
 duration=len(x)/rate
 result.append({'id':idx,'label':label,'file':filename,'duration':duration})
 records.append(f'{idx:02} | 视频 {1 if name=="one" else 2} | {a/rate:.2f}–{b/rate:.2f} 秒 | {label}')
 print(f'{idx:02} {name} {a/rate:.2f}–{b/rate:.2f}s gain={gain:.2f} {label}')
Path('Assets/clips.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
Path('音频切分记录.md').write_text('# 音频切分记录\n\n每段来自用户提供的两个视频，边界有少量重叠和淡入淡出，音量按均方根约 -20 dBFS 调整，避免过响。\n\n'+'\n'.join(records)+'\n')
