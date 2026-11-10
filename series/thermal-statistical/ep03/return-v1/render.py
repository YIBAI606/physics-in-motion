from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,math,json
P=Path(__file__).parent;BG='#0c1422';FG='#edf1f5';MUT='#9badbf';BLUE='#69b8dc';GOLD='#efb276'
F={n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n) for n in [24,28,32,38,44,48,64]}
C={'conditions':[(0,6,'如果材料比皮肤更热，刚才的结论会怎样？'),(6,13,'热流方向反过来，材料开始向皮肤传热。'),(13,20,'在相同初温下，热感受率较大的材料，往往让接触处温度更高。'),(20,27,'所以，金属并不是天生冷。它也可能让你觉得更烫。'),(27,34,'但在金属表面加上一层涂层，传热就可能受到阻碍。'),(34,41,'如果金属很薄，温度变化很快到达背面，也不能再当作无限厚。'),(41,48,'触感取决于材料，也取决于接触方式和时间。')],
'return':[(0,6,'现在，回到开头的两块冰。'),(6,13,'摸金属时，是你的手把热量传给金属。'),(13,20,'放上冰时，则是室温材料把热量传给更冷的冰。'),(20,27,'在相同条件下，材料能否更快供热，会影响冰融化的过程。'),(27,34,'但冰的初温、材料厚度、接触面积和融水层，都可能改变结果。'),(34,41,'所以，动画能解释机制。真实融化快慢，还要通过对照实验确认。'),(41,48,'摸起来更冷，不一定温度更低。要看接触之后，发生了什么。')]}
def tx(d,xy,s,n=38,c=FG,a=None):d.text(xy,s,font=F[n],fill=c,anchor=a)
def arrow(d,x,y1,y2,t):
 d.line((x,y1,x,y2),fill=GOLD,width=6);sign=1 if y2>y1 else -1;d.polygon([(x,y2),(x-13,y2-22*sign),(x+13,y2-22*sign)],fill=GOLD)
 for i in range(3):
  y=y1+(y2-y1)*((t*.5+i/3)%1);d.ellipse((x-5,y-5,x+5,y+5),fill=FG)
def block(d,x,y,wood=False):
 d.polygon([(x,y),(x+60,y-40),(x+540,y-40),(x+480,y)],fill='#967650' if wood else '#9dadb9')
 d.rectangle((x,y,x+480,y+140),fill='#6c5139' if wood else '#536b7e');d.polygon([(x+480,y),(x+540,y-40),(x+540,y+100),(x+480,y+140)],fill='#3d4147')
def frame(kind,t):
 im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im)
 tx(d,(90,45),'忆白 · 热与触感',24,MUT)
 if kind=='conditions':
  tx(d,(90,120),'把温差反过来，会怎样？' if t<27 else '换一个接触条件，结果也会变',48)
  tx(d,(90,200),'模型示意 · 温度为教学示例 · 不进行高温触摸实验',28,MUT)
  if t<27:
   for x,mat,e,c in [(230,'高热感受率材料',8000,BLUE),(1100,'低热感受率材料',450,GOLD)]:
    d.rounded_rectangle((x,340,x+530,500),radius=18,fill='#b4937d');d.rectangle((x,500,x+530,760),fill='#6d594e')
    tx(d,(x+25,370),'皮肤初温 32°C',32);tx(d,(x+25,690),'材料初温 40°C',32)
    tx(d,(x+265,830),mat,32,c,'mm')
    if t>=6:arrow(d,x+380,650,430,t)
    if t>=13:
     tc=(1200*32+e*40)/(1200+e);tx(d,(x+30,545),f'接触温度 ≈ {tc:.1f}°C',32)
  elif t<34:
   d.rounded_rectangle((360,320,1560,500),radius=20,fill='#b4937d');d.rectangle((360,500,1560,575),fill='#b9b39d');d.rectangle((360,575,1560,790),fill='#536b7e')
   tx(d,(400,370),'皮肤',38);tx(d,(400,518),'涂层 / 额外热阻',32,BG);tx(d,(400,680),'金属基底',38)
   tx(d,(960,860),'需要考虑分层材料与接触热阻',32,MUT,'mm')
  else:
   d.rectangle((300,440,1620,510),fill='#8496a5');tx(d,(300,360),'薄金属片',44)
   u=min(1,(t-34)/5);y=440+70*u
   d.rectangle((300,440,1620,y),fill='#c99b6b');d.line((300,510,1620,510),fill=FG,width=3)
   tx(d,(960,610),'温度变化到达背面',38,GOLD,'mm');tx(d,(960,720),'半无限体近似不再适用',44,FG,'mm')
   tx(d,(960,840),'示意范围变化，不是计算得到的温度场',28,MUT,'mm')
 else:
  tx(d,(90,120),'同一块材料，为什么能让冰融化？',48)
  tx(d,(90,200),'机制示意 · 尚无真实对照实验结果',28,MUT)
  if t<27:
   for x,wood in [(230,False),(1110,True)]:
    block(d,x,610,wood);d.rounded_rectangle((x+190,440,x+290,570),radius=10,fill='#b7e7f4',outline=FG,width=3)
    tx(d,(x+250,825),'木材 · 22°C' if wood else '金属 · 22°C',32,a='mm')
   if 6<=t<13:
    tx(d,(960,330),'手较热 → 材料较冷',44,GOLD,'mm')
   if t>=13:
    for x in [565,1445]:arrow(d,x,720,510,t)
    tx(d,(960,330),'材料较热 → 冰较冷',44,GOLD,'mm')
  elif t<41:
   labels=[('冰的初温','是否已经到达熔点'),('材料尺寸','厚度与总热容量'),('接触条件','面积、压力与水层'),('环境供热','空气、桌面与持续时间')]
   for i,(a,b) in enumerate(labels):
    if t<27+i*1.4:continue
    x=180+(i%2)*840;y=320+(i//2)*250
    d.rounded_rectangle((x,y,x+750,y+200),radius=20,fill='#1a2a3b');tx(d,(x+35,y+30),a,38,GOLD);tx(d,(x+35,y+110),b,32)
  else:
   tx(d,(960,460),'摸起来更冷',64,BLUE,'mm');tx(d,(960,600),'不一定温度更低',64,FG,'mm');tx(d,(960,770),'看接触之后，发生了什么',38,MUT,'mm')
 for a,b,s in C[kind]:
  if a<=t<b:
   if len(s)>34:
    k=s.find('，')+1
    if k<8:k=26
    tx(d,(960,958),s[:k],38,a='mm');tx(d,(960,1013),s[k:],38,a='mm')
   else:tx(d,(960,990),s,38,a='mm')
   break
 return im
if __name__=='__main__':
 for kind in C:
  p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(P/(kind+'-review.mp4'))],stdin=subprocess.PIPE)
  for i in range(48*30):p.stdin.write(frame(kind,i/30).tobytes())
  p.stdin.close();assert p.wait()==0
  (P/(kind+'-voiceover.txt')).write_text('\n\n'.join(s for a,b,s in C[kind]))
  (P/(kind+'.srt')).write_text('\n\n'.join(f'{i+1}\n00:00:{a:02},000 --> 00:00:{b:02},000\n{s}' for i,(a,b,s) in enumerate(C[kind])))
 sheet=Image.new('RGB',(1440,810),BG)
 for i,(k,t) in enumerate([('conditions',3),('conditions',16),('conditions',30),('conditions',39),('return',3),('return',16),('return',28),('return',36),('return',44)]):sheet.paste(frame(k,t).resize((480,270)),((i%3)*480,(i//3)*270))
 sheet.save(P/'review-sheet.jpg',quality=90)
 print('Done')
