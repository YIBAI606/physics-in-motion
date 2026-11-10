from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json
P=Path(__file__).parent; W,H=1920,1080; FPS=30
raw=Image.open(P/'finger-cartoon.png').convert('RGBA')
bbox=raw.getchannel('A').point(lambda a:255 if a>100 else 0).getbbox()
finger=raw.crop(bbox); finger.thumbnail((420,190),Image.Resampling.LANCZOS)
BG='#0c1422';WHITE='#edf1f5';MUT='#98acbf';HOT='#efb276';BLUE='#69b8dc'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fonts={n:ImageFont.truetype(font,n) for n in [26,30,36,42,48,64]}
cues=[(0,3.4,'摸起来，金属比木头冷。'),(3.4,7.6,'可在合适条件下，金属上的冰反而可能融得更快。'),(7.6,11.5,'因为你的手比室温材料热，热量从手流向材料。'),(11.5,15.5,'而材料比冰热，热量又能从材料流向冰。'),(15.5,19.5,'同一块金属，在两次接触中，分别接收和提供热量。'),(19.5,24.5,'所以，摸起来更冷，不一定意味着温度更低。'),(24.5,30,'真正要看的，是接触以后，你的手怎样失去热量。')]
(P/'voiceover.txt').write_text('\n\n'.join(c[2] for c in cues))
(P/'timeline.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
def stamp(t):return f'{int(t//3600):02}:{int(t//60)%60:02}:{int(t)%60:02},{round((t%1)*1000):03}'
(P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(cues)))
def txt(d,pos,s,n=36,c=WHITE,anchor=None):d.text(pos,s,font=fonts[n],fill=c,anchor=anchor)
def block(d,x,y,wood=False):
 c='#94734f' if wood else '#9daebb';face='#69503b' if wood else '#566b7c'
 d.polygon([(x,y),(x+70,y-45),(x+540,y-45),(x+470,y)],fill=c)
 d.rectangle((x,y,x+470,y+145),fill=face)
 d.polygon([(x+470,y),(x+540,y-45),(x+540,y+100),(x+470,y+145)],fill='#3a4149' if not wood else '#47372b')
 for i in range(7):d.line((x+15,y+20+i*17,x+450,y+20+i*17),fill=c,width=1)
def ice(d,x,y):
 d.rounded_rectangle((x,y,x+100,y+100),radius=10,fill='#9bd9ed',outline='#e0f7ff',width=3)
 d.line((x+15,y+15,x+70,y+15),fill='white',width=3)
def flow(d,x,y1,y2,t):
 d.line((x,y1,x,y2),fill=HOT,width=5)
 direction=1 if y2>y1 else -1
 d.line((x-14,y2-direction*20,x,y2),fill=HOT,width=5);d.line((x+14,y2-direction*20,x,y2),fill=HOT,width=5)
 for i in range(4):
  q=((t*.65+i/4)%1);y=y1+(y2-y1)*q;d.ellipse((x-5,y-5,x+5,y+5),fill='#ffe1ad')
def frame(t,caption=True):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 txt(d,(100,55),'忆白 · 热与触感',26,MUT)
 if t<7.6:
  txt(d,(100,140),'摸起来更冷，却可能让冰融得更快？',48)
  block(d,230,580);block(d,1110,580,True)
  txt(d,(460,795),'金属 · 22°C',36,anchor='mm');txt(d,(1340,795),'木材 · 22°C',36,anchor='mm')
  if t<3.4:
   u=min(1,t/1.2); eased=u*u*(3-2*u)
   y=560-finger.height-round(90*(1-eased))
   for x in [190,1070]:im.paste(finger,(x,y),finger)
   txt(d,(100,245),'触感不同',36,BLUE)
  else:
   p=min(1,(t-3.4)/.7);y=int(350+130*p);ice(d,425,y);ice(d,1305,y)
   txt(d,(100,245),'构图示意 · 融化结果需实验验证',30,MUT)
 elif t<19.5:
  txt(d,(100,140),'同一块材料，热量可以向两个方向传递',48)
  # Two complementary contacts, same material temperature.
  im.paste(finger,(300,440-finger.height),finger);txt(d,(760,350),'皮肤 · 32°C',30)
  block(d,280,650);block(d,1100,650)
  ice(d,1285,320)
  txt(d,(530,850),'材料 · 22°C',36,anchor='mm');txt(d,(1350,850),'材料 · 22°C',36,anchor='mm')
  txt(d,(1430,365),'冰 · 0°C',30)
  if t>=7.6:flow(d,530,455,610,t)
  if t>=11.5:flow(d,1335,610,455,t)
  if t>=15.5:txt(d,(960,250),'接收热量                       提供热量',36,HOT,'mm')
 else:
  txt(d,(100,140),'触感，不是温度计',64)
  if t<24.5:
   block(d,230,580);block(d,1110,580,True)
   txt(d,(490,380),'22°C',64,WHITE,'mm');txt(d,(1370,380),'22°C',64,WHITE,'mm')
   txt(d,(490,800),'金属',36,anchor='mm');txt(d,(1370,800),'木材',36,anchor='mm')
   txt(d,(960,400),'=',64,MUT,'mm')
  else:
   txt(d,(100,245),'放大接触处，看皮肤如何失去热量',36,MUT)
   d.rounded_rectangle((400,350,1520,550),radius=18,fill='#a97e66')
   d.rectangle((400,550,1520,810),fill='#52697b')
   txt(d,(440,400),'皮肤',36);txt(d,(440,725),'材料',36)
   for x in [750,1000,1250]:flow(d,x,470,690,t)
 if caption:
  for a,b,s in cues:
   if a<=t<b:txt(d,(960,990),s,42,WHITE,'mm');break
 return im
if __name__=='__main__':
 cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'opening-30s-review.mp4')]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for i in range(900):p.stdin.write(frame(i/30).tobytes())
 p.stdin.close();assert p.wait()==0
 sheet=Image.new('RGB',(1440,810),BG)
 for i,t in enumerate([1.5,5,9,13,17,22,25,27,29]):sheet.paste(frame(t).resize((480,270)),((i%3)*480,(i//3)*270))
 sheet.save(P/'review-sheet.jpg',quality=90)
 print('Rendered 900 frames')
