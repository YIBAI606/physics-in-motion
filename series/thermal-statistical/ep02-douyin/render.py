from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from functools import lru_cache
import math,subprocess,json
R=Path(__file__).resolve().parent
BG='#101722';WHITE='#eef3fa';MUTED='#a6b5c9';ORANGE='#ffb45e';BLUE='#64baff';GREEN='#7be0bd'
@lru_cache(None)
def font(n,b=False):return ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-'+('Bold' if b else 'Regular')+'.ttc',n)
cues=[(0,3,'温度一样，能量却能差一倍？'),(3,7,'看这两组完全相同的小振子。'),(7,10.5,'左边的数量，是右边的两倍。'),(10.5,14,'在同样的温度下，'),(14,18,'每个振子的平均能量相同。'),(18,23,'所以，左边的平均总能量，\n也是右边的两倍。'),(23,25.5,'注意，是平均。'),(25.5,29,'每个振子的能量仍然会变化，'),(29,33,'并不是大家时时刻刻\n都分到一样多。'),(33,36,'热平衡要求温度相同，'),(36,39.5,'不要求总能量相同。'),(40,43.5,'那温度，究竟衡量什么？')]
def timestamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{timestamp(a)} --> {timestamp(b)}\n{s}' for i,(a,b,s) in enumerate(cues))+'\n',encoding='utf-8')
(R/'voiceover.txt').write_text('\n\n'.join(s.replace('\n','') for a,b,s in cues),encoding='utf-8')
(R/'timeline.json').write_text(json.dumps([dict(start=a,end=b,text=s) for a,b,s in cues],ensure_ascii=False,indent=2),encoding='utf-8')
def frame(t):
 im=Image.new('RGB',(540,960),BG);d=ImageDraw.Draw(im)
 def text(x,y,s,n=22,c=WHITE,b=False):d.text((x,y),s,font=font(n,b),fill=c,anchor='mm')
 text(245,55,'不会物理的忆白',17,MUTED)
 title='温度一样，能量能差一倍？' if t<10.5 else '先看每个振子的平均值' if t<18 else '数量翻倍，总量也翻倍' if t<23 else '平均相同 ≠ 每次相同' if t<33 else '同温，不必同能量' if t<40 else '温度，究竟衡量什么？'
 text(250,111,title,27,WHITE,True)
 if t>=40:
  text(250,340,'温度',54,GREEN,True)
  text(250,430,'不是能量的多少',29,WHITE)
  text(250,565,'下一期，接着看。',23,MUTED)
  return im
 per=10.5<=t<18; fluctuations=23<=t<33
 xs=[140,370]
 for side,x in enumerate(xs):
  c=ORANGE if side==0 else BLUE;n=12 if side==0 else 6
  text(x,177,'同一温度 T',19,GREEN)
  d.rounded_rectangle((x-91,207,x+91,424),radius=15,outline='#344358',width=2)
  for k in range(n):
   px=x+(k%3-1)*43;py=252+(k//3)*43
   dx=5*math.sin(t*3+k*1.4+side)
   d.line((px-12,py,px+12,py),fill='#40506a',width=2)
   d.ellipse((px+dx-6,py-6,px+dx+6,py+6),fill=c)
   if 7<=t<10.5:
    pulse=(t-7)/3.5
    if k<int(pulse*n)+1:d.ellipse((px-14,py-14,px+14,py+14),outline=c,width=2)
  text(x,452,f'{n} 个相同振子',19,c)
 if fluctuations:
  text(250,502,'单个振子的能量变化示意',19,MUTED)
  base=700;mean=90
  for side,x in enumerate(xs):
   c=ORANGE if side==0 else BLUE
   val=mean*(1+.65*math.sin((t-23)*2+side*2))
   d.rectangle((x-25,base-val,x+25,base),fill=c)
   text(x,728,'某一个振子',17,MUTED)
  for x in range(55,455,14):d.line((x,base-mean,x+7,base-mean),fill=GREEN,width=2)
  text(250,760,'虚线：相同的平均值',17,GREEN)
 else:
  for side,x in enumerate(xs):
   c=ORANGE if side==0 else BLUE
   value=1 if per else (2 if side==0 else 1)
   bh=75*value;base=700
   d.rounded_rectangle((x-33,base-bh,x+33,base),radius=5,fill=c)
   text(x,base-bh-23,'相同' if per else ('2E' if side==0 else 'E'),24,c,True)
   text(x,730,'每个振子的平均能量' if per else '平均总能量',16,MUTED)
  if per:text(250,506,'比较相同振子，在同一温度下的平均值',17,GREEN)
  elif 18<=t<23:text(250,506,'12 × 每个平均值       6 × 每个平均值',17,GREEN)
 text(250,905,'相同频率振子；能量以基态为零；示意图',12,MUTED)
 return im
if __name__=='__main__':
 fps=24;duration=45
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(fps),'-i','-','-an','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'douyin-clean.mp4')]
 p=subprocess.Popen(args,stdin=subprocess.PIPE)
 for i in range(fps*duration):
  im=frame(i/fps);p.stdin.write(im.tobytes())
  if i in [0,15*fps,27*fps,37*fps,42*fps]:im.save(R/f'frame-{i//fps:02}.png')
 p.stdin.close();assert p.wait()==0
 print('Clean video complete',flush=True)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(R/'douyin-clean.mp4'),'-vf',"subtitles="+str(R/'captions.srt')+":force_style='FontName=Noto Sans CJK SC,FontSize=8,PrimaryColour=&H00FAF3EE,OutlineColour=&H00221710,BorderStyle=1,Outline=1,Shadow=0,Alignment=2,MarginV=35,MarginL=18,MarginR=28'",'-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'douyin-review.mp4')],check=True)
 print('Captioned video complete',flush=True)
