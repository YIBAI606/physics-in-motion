from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,subprocess,json
P=Path(__file__).parent;BG='#0c1422';FG='#edf1f5';MUT='#9badbf';GOLD='#efb276';BLUE='#69b8dc'
F={n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n) for n in [24,28,32,38,44,48,64]}
C={'black':[(0,6,'热量进入物体，却没有让温度继续上升。这个疑问并不新。'),(6,13,'十八世纪，约瑟夫·布莱克研究了潜热和比热。'),(13,20,'在后来整理出版的讲义里，他讨论了冰融化时吸收的热量。'),(20,27,'这些热量，并没有全部表现为温度计上更高的读数。'),(27,34,'温度变化和热量传递，因此不能简单画上等号。'),(34,40,'用今天的语言说，热量也可以用于相变。')],
'fourier':[(0,7,'知道热会从高温处流向低温处，还不等于知道它流得多快。'),(7,14,'十九世纪初，傅里叶研究了怎样用数学描述热在物体中的传播。'),(14,21,'一八二二年，他出版了《热的解析理论》。'),(21,28,'我们今天使用的热传导模型，继承了这条把温度变化变成数学问题的路线。'),(28,34,'给定初始温度和接触条件，就可以计算内部温度怎样变化。'),(34,40,'接下来，我们就在皮肤内部选一个位置，看看它的温度。')],
'ending':[(1,6,'可有些“冷”，我们不敢再问。'),(7,15,'比如，一个原本无话不谈的人，后来只回了一句：“嗯。”'),(17,21,'我们知道自己难过了。'),(21,26,'却不一定知道，对方为什么沉默。'),(26,35,'可能是疲惫，可能是不知道怎么开口，也可能，那段关系确实变了。'),(36,40,'物理解释不了这些。'),(41,47,'但拍完这期，我想留给自己一个提醒：'),(47,55,'感受值得认真对待，对感受的解释，可以慢一点。'),(55,60,'不必急着替沉默写好结局。'),(60,64,'如果还想知道，也许可以问一句：'),(64,68,'“最近，你还好吗？”'),(70,75,'我是忆白，和你一起，让理解发生。')]}
D={'black':40,'fourier':40,'ending':77}
def tx(d,xy,s,n=38,c=FG,a=None):d.text(xy,s,font=F[n],fill=c,anchor=a)
def frame(k,t):
 im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im)
 if k=='black':
  tx(d,(100,80),'热量，未必都写在温度计上',48)
  tx(d,(100,190),'Joseph Black · 约瑟夫·布莱克',38,GOLD)
  tx(d,(100,260),'1728—1799',28,MUT)
  d.line((220,390,220,780),fill=MUT,width=8);d.ellipse((195,755,245,805),fill=BLUE)
  d.line((220,620,220,780),fill=BLUE,width=16);tx(d,(280,610),'温度读数',32,BLUE)
  for i in range(5):
   x=800+i*140;y=510;d.rounded_rectangle((x,y,x+100,y+100),radius=10,fill='#a5d9e8')
   if t>13+i*2:d.rounded_rectangle((x,y+110,x+100,y+140),radius=12,fill='#397b9b')
  tx(d,(1100,750),'吸热 → 相变',44,GOLD,'mm')
  tx(d,(100,875),'依据：Black《化学原理讲义》（1803）潜热节；现代示意，非原书扫描',24,MUT)
 elif k=='fourier':
  tx(d,(100,80),'从“会传热”，到“能预测”',48)
  tx(d,(100,190),'Joseph Fourier · 约瑟夫·傅里叶',38,GOLD)
  tx(d,(100,260),'1822 · Théorie analytique de la chaleur',28,MUT)
  # schematic smooth decay of a localized warm initial profile
  for j in range(900):
   x=(j-450)/180;v=math.exp(-x*x/(1+t/8))/math.sqrt(1+t/8)
   c=tuple(round(a+(b-a)*v) for a,b in zip((66,135,190),(239,178,118)))
   d.line((510+j,420,510+j,600),fill=c)
  tx(d,(960,710),'初始温度 + 边界条件 → 温度随时间变化',38,FG,'mm')
  tx(d,(100,875),'依据：MacTutor 傅里叶传记；1822年著作出版记录。图为现代数学示意',24,MUT)
 else:
  # Restrained lights stay separated. No implication of reconciliation.
  layer=Image.new('RGB',(1920,1080),BG);ld=ImageDraw.Draw(layer)
  a=min(1,t/2)
  for x in [650,1270]:
   for r in range(160,0,-5):
    v=.12*a*math.exp(-((r/65)**2));c=tuple(round(b+(h-b)*v) for b,h in zip((12,20,34),(239,178,118)))
    ld.ellipse((x-r,440-r,x+r,440+r),fill=c)
   ld.ellipse((x-5,435,x+5,445),fill=(round(239*a),round(190*a),round(135*a)))
  im=layer;d=ImageDraw.Draw(im)
  if 47<=t<60:
   tx(d,(960,670),'感受值得认真对待',44,FG,'mm');tx(d,(960,750),'对感受的解释，可以慢一点',38,MUT,'mm')
  if t>=68:
   # Callback uses the approved cartoon asset and original opening geometry.
   import sys
   sys.path.insert(0,'/workspace/work/ep03-opening-v2');import render as unused
   finger=Image.open('/workspace/work/ep03-opening-v2/finger-cartoon.png').convert('RGBA');bbox=finger.getchannel('A').point(lambda a:255 if a>100 else 0).getbbox();finger=finger.crop(bbox);finger.thumbnail((420,190),Image.Resampling.LANCZOS)
   d.rectangle((710,600,1230,760),fill='#536b7e');im.paste(finger,(690,600-finger.height-12),finger)
   if t>=70:tx(d,(960,835),'让理解发生',44,FG,'mm')
 for a,b,s in C[k]:
  if a<=t<b:
   if len(s)>32:
    split=s.find('，')+1
    if split<8:split=26
    tx(d,(960,957),s[:split],38,a='mm');tx(d,(960,1012),s[split:],38,a='mm')
   else:tx(d,(960,990),s,38,a='mm')
   break
 return im
if __name__=='__main__':
 for k in C:
  p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(P/(k+'-review.mp4'))],stdin=subprocess.PIPE)
  for i in range(D[k]*30):p.stdin.write(frame(k,i/30).tobytes())
  p.stdin.close();assert p.wait()==0
  (P/(k+'-voiceover.txt')).write_text('\n\n'.join(s for a,b,s in C[k]))
  stamp=lambda t:f'00:{int(t)//60:02}:{int(t)%60:02},000'
  (P/(k+'.srt')).write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(C[k])))
 print('Narrative segments rendered')
