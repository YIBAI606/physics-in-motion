from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
from pathlib import Path
import numpy as np,math,subprocess,json
R=Path(__file__).parent;W,H=1920,1080
BG=(14,21,31);FG='#edf1f3';MUTED='#9aa9b8';GOLD='#e9c775'
@lru_cache(None)
def font(n,b=False):return ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-'+('Bold' if b else 'Regular')+'.ttc',n)
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def mix(a,b,p):return tuple(round(x+(y-x)*p) for x,y in zip(a,b))
def color(T):
 p=max(0,min(1,(T-22)/10));return mix((83,141,192),(212,216,213),p*2) if p<.5 else mix((212,216,213),(229,155,101),(p-.5)*2)
# Illustrative ideal properties; not measured skin or specific material samples.
materials=[dict(name='金属',e=8000,alpha=1.2e-5),dict(name='木头',e=450,alpha=1.3e-7)]
for m in materials:m['Tc']=(1200*32+m['e']*22)/(1200+m['e'])
(R/'model.json').write_text(json.dumps(dict(assumptions=['一维半无限介质','恒定物性','完美接触','无血流与接触热阻','参数仅用于模型示意'],skin=dict(initial_C=32,e=1200,alpha=1.1e-7),objects_initial_C=22,materials=materials),ensure_ascii=False,indent=2))
def frame(t):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 def txt(x,y,s,n=38,c=FG,b=False,anchor='mm'):d.text((x,y),s,font=font(n,b),fill=c,anchor=anchor)
 txt(90,54,'忆白 / 热统',25,MUTED,anchor='lm')
 if t<8:
  txt(960,155,'一样的温度，不一样的触感',58,FG,True)
  for i,cx in enumerate([500,1420]):
   # Matching geometry; material colors never encode temperature.
   x=cx-290;y=460
   d.ellipse((x-10,y+265,x+650,y+330),fill='#0a1018')
   d.polygon([(x,y),(x+540,y),(x+640,y-95),(x+100,y-95)],fill='#c0c7cd' if i==0 else '#b09d83')
   d.polygon([(x+540,y),(x+640,y-95),(x+640,y+175),(x+540,y+270)],fill='#414b57' if i==0 else '#62513f')
   for row in range(270):
    v=row/269
    col=mix((163,176,185),(76,88,102),v) if i==0 else mix((155,134,103),(117,97,76),v)
    d.line((x,y+row,x+540,y+row),fill=col)
   if i==0:
    d.line((x,y,x+540,y,x+640,y-95),fill='#e3e9ed',width=3)
    for yy in range(y+10,y+260,12):d.line((x+8,yy,x+532,yy),fill=(130,145,157),width=1)
   else:
    for k in range(8):
     pts=[(x+z,y+25+k*28+int(7*math.sin(z/90+k))) for z in range(8,533,4)]
     d.line(pts,fill='#715b43',width=2)
   txt(cx,800,'金属' if i==0 else '木头',36,MUTED)
   txt(cx,868,'初始 22 °C',45,'#b9d4e6',True)
   if t>=3:
    p=ease((t-3)/2);bottom=285+175*p
    d.rounded_rectangle((cx-52,230,cx+52,bottom),radius=45,fill='#c9ae99',outline='#ead6c4',width=2)
    d.rounded_rectangle((cx-32,bottom-85,cx+32,bottom-25),radius=19,fill='#e2cabb')
  subtitle='同室放置足够久，初始温度相同。' if t<3 else '为什么金属摸起来更冷？'
  txt(960,990,subtitle,40,FG,True)
 else:
  tau=max(.03,(t-8)*.65)
  txt(960,135,'看接触面：手的降温过程不同',55,FG,True)
  txt(960,202,'相同初始温度 · 同一时间标尺 · 同一温标',29,MUTED)
  for i,m in enumerate(materials):
   x0=100+i*940;xc=x0+340;y0=370;hh=310;width=780;tc=m['Tc']
   txt(x0+390,290,m['name'],42,FG,True)
   xs=np.arange(width);distance=np.abs(xs-340)*(.008/440)
   arr=[]
   for z,dist in enumerate(distance):
    initial,alpha=(32,1.1e-7) if z<340 else (22,m['alpha'])
    T=initial+(tc-initial)*math.erfc(dist/(2*math.sqrt(alpha*tau)))
    arr.append(color(T))
   strip=Image.fromarray(np.array([arr],dtype=np.uint8),'RGB').resize((width,hh))
   im.paste(strip,(x0,y0));d=ImageDraw.Draw(im)
   for yy in range(y0-15,y0+hh+15,22):d.line((xc,yy,xc,yy+10),fill='#ffffff',width=2)
   txt(x0+150,730,'皮肤侧',30,MUTED);txt(x0+570,730,'材料内部',30,MUTED)
   txt(xc,335,'接触面',26,MUTED)
   # Arrow indicates direction only, not quantitative flux.
   ax=xc-95;ay=525
   d.line((ax,ay,ax+190,ay),fill='#172534',width=6)
   d.polygon([(ax+190,ay),(ax+170,ay-13),(ax+170,ay+13)],fill='#172534')
   txt(x0+390,795,'热量从手传向材料',28,FG)
  # Unified legend with absolute model scale.
  for px in range(440):d.line((740+px,870,740+px,891),fill=color(22+10*px/439))
  txt(705,880,'22°C',24,MUTED,anchor='rm');txt(1210,880,'32°C',24,MUTED,anchor='lm')
  txt(960,940,'热量传得不同，皮肤的降温也不同。',39,FG,True)
  txt(960,1015,f'理想接触模型示意 · 模型时间 {tau:.1f} s · 非实测数据',23,MUTED)
 return im
if __name__=='__main__':
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'ep03-contact-22s.mp4')],stdin=subprocess.PIPE)
 for i in range(22*30):
  im=frame(i/30);p.stdin.write(im.tobytes())
  if i in [60,180,330,600]:im.save(R/f'frame-{i//30:02}.png')
 p.stdin.close();assert p.wait()==0;print('DONE',flush=True)
