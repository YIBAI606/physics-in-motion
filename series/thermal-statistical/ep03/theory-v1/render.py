from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,math,json
P=Path(__file__).parent;BG='#0c1422';FG='#edf1f5';MUT='#9badbf';BLUE='#69b8dc';GOLD='#efb276'
F={n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n) for n in [24,28,32,38,44,48,64,80]}
C={
'latent':[(0,5,'冰吸收热量，温度就一定会上升吗？'),(5,11,'如果纯冰已经到达熔点，继续吸热，可以用于融化。'),(11,17,'在近标准大气压、冰水共存时，温度可以维持在零摄氏度附近。'),(17,23,'这时，热量增加，主要表现为更多的冰变成水。'),(23,29,'融化多少冰，取决于吸收的热量，以及熔化潜热。'),(29,35,'融化一克已经达到熔点的冰，大约需要三百三十四焦耳。'),(35,40,'如果冰还低于零度，就不能省略先升温所需的热量。')],
'effusivity':[(0,5,'为什么同样的温度，接触后却会出现不同的降温？'),(5,11,'只知道材料导热快不快，还不够。'),(11,17,'还要知道，同样体积的材料，升温需要多少热量。'),(17,23,'导热系数和体积热容量，共同组成热感受率。'),(23,29,'在理想接触模型里，接触温度是两侧初温的加权平均。'),(29,35,'哪一侧的热感受率更大，接触温度就更靠近哪一侧。'),(35,41,'室温金属的热感受率较大，就能让接触处更接近它的温度。'),(41,46,'但这是理想模型。涂层、接触热阻和厚度，都可能改变结果。')]}
def tx(d,xy,s,n=38,c=FG,anchor=None):d.text(xy,s,font=F[n],fill=c,anchor=anchor)
def flow(d,x,y1,y2,t):
 d.line((x,y1,x,y2),fill=GOLD,width=5);d.polygon([(x,y2),(x-13,y2-20),(x+13,y2-20)],fill=GOLD)
 for i in range(3):
  y=y1+(y2-y1)*((t*.5+i/3)%1);d.ellipse((x-5,y-5,x+5,y+5),fill=GOLD)
def frame(kind,t):
 im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im)
 tx(d,(90,45),'忆白 · 热与触感',24,MUT)
 if kind=='latent':
  tx(d,(90,120),'吸收热量，也可以用来融化',48)
  tx(d,(90,200),'纯冰已达熔点 · 近标准大气压 · 能量关系示意',28,MUT)
  # Melting progresses only while supplying latent heat; qualitative amount, not a speed model.
  p=max(0,min(1,(t-11)/18));remaining=1-.7*p
  x,y,w,h=240,410,660,360
  water=round(h*(1-remaining));d.rectangle((x,y+h-water,x+w,y+h),fill='#377699')
  iw=round(250*remaining**.5);ih=round(240*remaining**.5)
  d.rounded_rectangle((570-iw//2, min(760-ih,770-water-ih*.15),570+iw//2,min(760,770-water+ih*.85)),radius=12,fill='#b6e7f4',outline='#e6f7fc',width=3)
  d.line((x,y,x,y+h,x+w,y+h,x+w,y),fill=MUT,width=4)
  if 5<t<35:
   flow(d,560,290,390,t)
  tx(d,(570,840),'0°C 附近 · 冰水共存',32,anchor='mm')
  tx(d,(1090,350),'温度',32,MUT);tx(d,(1090,410),'≈ 0°C',64,BLUE)
  tx(d,(1090,550),'用于融化的累计热量',32,MUT)
  d.rounded_rectangle((1090,610,1700,645),radius=8,fill='#263648')
  if p>0:d.rounded_rectangle((1090,610,1090+610*p,645),radius=8,fill=GOLD)
  if t>=23:tx(d,(1090,710),'Q = m L',64);tx(d,(1090+d.textlength('Q = m L',font=F[64])+2,752),'f',28)
  if t>=29:tx(d,(1090,825),'1 g 冰 → 约 334 J',38,GOLD)
  if t>=35:
   d.rectangle((180,300,940,815),fill=BG)
   tx(d,(560,460),'−18°C → 0°C',64,anchor='mm');tx(d,(560,570),'先升温，再考虑融化',38,GOLD,'mm')
 else:
  tx(d,(90,120),'接触表现，由导热与储热共同决定',48)
  tx(d,(90,200),'理想半无限体 · 常物性 · 完美接触 · 教学参数，非实测',28,MUT)
  if t<23:
   d.rounded_rectangle((170,330,870,730),radius=25,fill='#17293a');d.rounded_rectangle((1050,330,1750,730),radius=25,fill='#302b27')
   tx(d,(520,420),'k',80,BLUE,'mm');tx(d,(520,525),'导热系数',44,FG,'mm');tx(d,(520,625),'温度梯度如何产生热流',28,MUT,'mm')
   if t>=11:
    tx(d,(1400,420),'ρc',80,GOLD,'mm');tx(d,(1400,525),'体积热容量',44,FG,'mm');tx(d,(1400,625),'单位体积升温需要多少热量',28,MUT,'mm')
   if t>=17:tx(d,(960,835),'e = √(kρc)',64,FG,'mm')
  else:
   # A pedagogical parameter sweep, not evolution in physical time.
   u=max(0,min(1,(t-29)/9));e=450+(8000-450)*u;tc=(1200*32+e*22)/(1200+e)
   d.text((960,320),'T* = (e₁T₁ + e₂T₂) / (e₁ + e₂)',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',48),fill=FG,anchor='mm')
   x0,x1,y=300,1620,550
   d.line((x0,y,x1,y),fill=MUT,width=8)
   for x,label,c in [(x0,'材料初温 22°C',BLUE),(x1,'皮肤初温 32°C',GOLD)]:
    d.ellipse((x-12,y-12,x+12,y+12),fill=c);tx(d,(x,630),label,32,c,'mm')
   x=x0+(tc-22)/10*(x1-x0);d.ellipse((x-17,y-17,x+17,y+17),fill=FG)
   tx(d,(x,470),f'{tc:.1f}°C',44,FG,'mm')
   tx(d,(960,745),f'材料热感受率：{e:.0f}    |    皮肤：1200',32,FG,'mm')
   tx(d,(960,810),'参数变化演示，不是同一材料随时间改变',28,MUT,'mm')
   tx(d,(960,855),'热感受率单位：J / (m² · K · √s)',24,MUT,'mm')
 for a,b,s in C[kind]:
  if a<=t<b:
   if len(s)>34:
    k=s.find('，')+1
    if k<8:k=26
    tx(d,(960,957),s[:k],38,anchor='mm');tx(d,(960,1012),s[k:],38,anchor='mm')
   else:tx(d,(960,990),s,38,anchor='mm')
   break
 return im
if __name__=='__main__':
 for kind in C:
  duration=C[kind][-1][1]
  p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(P/(kind+'-review.mp4'))],stdin=subprocess.PIPE)
  for i in range(duration*30):p.stdin.write(frame(kind,i/30).tobytes())
  p.stdin.close();assert p.wait()==0
  (P/(kind+'-voiceover.txt')).write_text('\n\n'.join(s for a,b,s in C[kind]))
  stamp=lambda t:f'00:00:{int(t):02},000'
  (P/(kind+'.srt')).write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(C[kind])))
 sheet=Image.new('RGB',(1440,810),BG)
 for i,(k,t) in enumerate([('latent',3),('latent',15),('latent',30),('latent',37),('effusivity',7),('effusivity',19),('effusivity',25),('effusivity',33),('effusivity',39)]):sheet.paste(frame(k,t).resize((480,270)),((i%3)*480,(i//3)*270))
 sheet.save(P/'review-sheet.jpg',quality=90)
 print('Finished two segments')
