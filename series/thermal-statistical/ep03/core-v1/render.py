from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,csv
P=Path(__file__).parent;BG='#0c1422';FG='#edf1f5';MUT='#9badbf';BLUE='#69b8dc';GOLD='#efb276'
fonts={n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n) for n in [24,28,32,38,44,48]}
cues=[(0,5,'把接触处放大，先看皮肤和材料内部的温度。'),(5,10,'两块材料初始温度相同，皮肤的初始温度也相同。'),(10,15,'接触后，温度变化从接触面向内部扩展。'),(15,21,'现在，在皮肤内部选同一个深度，记录这里的温度。'),(21,27,'接触金属时，这个位置的温度下降得更明显。'),(27,33,'注意，曲线表示皮肤内部的温度，不是界面温度。'),(33,40,'这解释了冷感的一个重要原因。但具体触感，还受接触条件和生理反应影响。')]
params={'metal':(8000,1.2e-5),'wood':(450,1.3e-7)}
def T(mat,x,t,skin=True):
 ti=32 if skin else 22
 if t<=0:return ti
 e,a=params[mat];tc=(1200*32+e*22)/(1200+e);a=1.1e-7 if skin else a
 return ti+(tc-ti)*math.erfc(x/(2*math.sqrt(a*t)))
def color(T):
 f=max(0,min(1,(T-22)/10));return tuple(round(a+(b-a)*f) for a,b in zip((66,135,190),(239,178,118)))
def text(d,xy,s,n=32,c=FG,anchor=None):d.text(xy,s,font=fonts[n],fill=c,anchor=anchor)
def model_time(t):return max(0,min(5,(t-10)/4))
def frame(t,caption=True):
 im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im);tm=model_time(t)
 text(d,(80,45),'忆白 · 接触之后',24,MUT);text(d,(80,110),'同一个深度，皮肤会怎样降温？',48)
 text(d,(80,185),'理想模型 · 教学参数，非实测 · 两侧各显示 2 mm',28,MUT)
 text(d,(1710,185),f't = {tm:.2f} s',28,anchor='ra')
 for x,mat,name,c in [(160,'metal','接触金属',BLUE),(650,'wood','接触木材',GOLD)]:
  text(d,(x,275),name,38,c)
  for j in range(440):
   skin=j<220;depth=abs(j+.5-220)/220*.002
   d.line((x,340+j,x+320,340+j),fill=color(T(mat,depth,tm,skin)))
  d.line((x,560,x+320,560),fill=FG,width=2)
  text(d,(x+15,365),'皮肤',28,'#142535');text(d,(x+15,725),'材料',28,'#edf1f5')
  if t>=15:
   y=560-.00015/.002*220
   d.ellipse((x+245-8,y-8,x+245+8,y+8),fill=FG,outline='#0c1422',width=2)
   d.line((x+245,y,x+355,y),fill=FG,width=2)
   text(d,(x,820),'观察深度：0.15 mm',28)
 # Colorbar constant across all fields and time
 for j in range(300):d.line((200+j,885,200+j,900),fill=color(22+j/299*10))
 text(d,(110,878),'22°C',24);text(d,(520,878),'32°C',24)
 x0,y0,w,h=1120,780,670,420
 for temp in [22,24,26,28,30,32]:
  y=y0-(temp-22)/10*h;d.line((x0,y,x0+w,y),fill='#263648',width=1);text(d,(x0-22,y),str(temp),24,MUT,'rm')
 d.line((x0,340,x0,y0),fill=MUT,width=2);d.line((x0,y0,x0+w,y0),fill=MUT,width=2)
 for v in range(6):text(d,(x0+v/5*w,y0+20),str(v),24,MUT,'mt')
 text(d,(x0,290),'皮肤内部温度 / °C',28);text(d,(x0+w,835),'模型时间 / s',24,MUT,'ra')
 if t>=15:
  for mat,c in [('metal',BLUE),('wood',GOLD)]:
   pts=[(x0+v/500*w,y0-(T(mat,.00015,v/100)-22)/10*h) for v in range(int(tm*100)+1)]
   if len(pts)>1:d.line(pts,fill=c,width=5)
   if pts:
    x,y=pts[-1];d.ellipse((x-6,y-6,x+6,y+6),fill=c)
  text(d,(1150,875),'金属',28,BLUE);text(d,(1340,875),'木材',28,GOLD)
 else:text(d,(1240,520),'即将追踪同一观察点',28,MUT)
 if caption:
  for a,b,s in cues:
   if a<=t<b:
    if len(s)>34:
     k=s.find('。')+1
     if k<8 or k>34:k=30
     text(d,(960,962),s[:k],38,anchor='mm');text(d,(960,1015),s[k:],38,anchor='mm')
    else:text(d,(960,990),s,38,anchor='mm')
    break
 return im
if __name__=='__main__':
 p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'core-40s-review.mp4')],stdin=subprocess.PIPE)
 for i in range(1200):p.stdin.write(frame(i/30).tobytes())
 p.stdin.close();assert p.wait()==0
 sheet=Image.new('RGB',(1440,810),BG)
 for i,t in enumerate([0,8,12,16,20,24,28,32,38]):sheet.paste(frame(t).resize((480,270)),((i%3)*480,(i//3)*270))
 sheet.save(P/'review-sheet.jpg',quality=90)
 (P/'voiceover.txt').write_text('\n\n'.join(s for a,b,s in cues))
 (P/'timeline.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
 def stamp(t):return f'00:00:{int(t):02},000'
 (P/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(cues)))
 with (P/'model.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['time_s','metal_skin_C','wood_skin_C'])
  for i in range(501):w.writerow([i/100,T('metal',.00015,i/100),T('wood',.00015,i/100)])
 print('Rendered 1200 frames')
