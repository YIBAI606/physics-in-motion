from pathlib import Path
from PIL import Image,ImageDraw
import math,subprocess,json
import visual_base as v
R=Path(__file__).parent
cues=[(0,7,'一块金属，一块木头，在同一个房间里放了很久。'),(7,14,'它们的温度可以几乎一样。可摸上去，金属却明显更冷。'),(14,21,'温度一样，为什么感觉不一样？先别盯着物体，看你的手。'),(21,29,'通常，皮肤比室温下的材料更暖。接触之后，热量从手传向它们。'),(29,37,'你感觉到的冷，和皮肤怎样降温有关。初始温度相同，不代表降温过程相同。'),(37,45,'先看木头。它不容易把接触处收到的热量，迅速传向内部。'),(45,53,'靠近手的局部区域比较容易暖起来。它和皮肤之间的温差随之减小。'),(53,61,'金属则更容易把热量传向内部，让更多内部材料参与吸收热量。'),(61,69,'在常见条件下，金属会让接触附近的皮肤降温更明显，所以我们觉得它更冷。'),(69,77,'把同一深度的皮肤温度画出来，两个过程的差别就更清楚了。'),(77,85,'不过，差别不只由导热快慢决定。材料升温需要吸收多少热量，也会影响结果。'),(85,93,'短时间接触时，可以用一个结合这些因素的量来比较，叫热感受率。'),(93,101,'它同时考虑导热系数、密度和比热容。常见金属的热感受率通常比木头大。'),(101,109,'但这不意味着，金属总是摸起来更冷。如果材料一开始比手更热呢？'),(109,117,'热量就会反过来传向手。在合适的接触条件下，金属也可能显得更烫。'),(117,125,'所以，摸起来冷，不一定温度更低。还要看接触后，皮肤怎样失去热量。'),(125,133,'你的手能感受冷热，却不能只凭触感，准确比较不同材料的温度。'),(133,142,'你可以把金属勺和木制品放在同一房间足够久，再比较触感。但触摸不能证明温度完全相同。'),(142,150,'下一期，我们再问：温度，为什么决定热量传递的方向？'),(150,157,'我是忆白，和你一起，让理解发生。')]
def ts(t):return f'00:{int(t)//60:02}:{int(t)%60:02},000'
def wrap(s,n=26):
 if len(s)<=n:return s
 k=max([i+1 for i,c in enumerate(s[:n]) if c in '，。？：'] or [n]);return s[:k]+'\n'+wrap(s[k:],n)
(R/'voiceover.txt').write_text('\n\n'.join(c[2] for c in cues))
(R/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{ts(a)} --> {ts(b)}\n{wrap(s)}' for i,(a,b,s) in enumerate(cues))+'\n')
(R/'timeline.json').write_text(json.dumps([dict(start=a,end=b,text=s) for a,b,s in cues],ensure_ascii=False,indent=2))
def blank(title):
 im=Image.new('RGB',(1920,1080),v.BG);d=ImageDraw.Draw(im)
 d.text((90,54),'忆白 / 热统',font=v.font(25),fill=v.MUTED,anchor='lm')
 d.text((960,135),title,font=v.font(56,True),fill=v.FG,anchor='mm');return im

def frame(t):
 if t<21:
  im=v.frame(min(7.9,t*.55));d=ImageDraw.Draw(im);d.rectangle((0,925,1920,1080),fill=v.BG)
  if t>=14:
   # Focus changes, preserving the material scene.
   d.rectangle((0,95,1920,205),fill=v.BG);d.text((960,155),'先看手：它比材料更暖',font=v.font(56,True),fill=v.FG,anchor='mm')
  return im
 if t<69:
  # Same model time across both comparison panels. Later comparisons hold at 4 seconds.
  tau=min(6,max(.03,(t-21)*.5))
  im=v.frame(8+tau/.65);d=ImageDraw.Draw(im)
  d.rectangle((0,925,1920,1080),fill=v.BG)
  if 37<=t<53:
   d.rounded_rectangle((1025,265,1835,820),radius=12,outline=v.GOLD,width=3)
  elif 53<=t<69:d.rounded_rectangle((85,265,895,820),radius=12,outline=v.GOLD,width=3)
  d.text((960,913),f'理想接触模型 · 时间 {tau:.1f}s · 物性参数为教学示例，非实测',font=v.font(23),fill=v.MUTED,anchor='mm')
  return im
 if t<77:
  im=blank('同一皮肤深度，降温过程不同');d=ImageDraw.Draw(im)
  left,right,top,bottom=240,1640,270,780
  d.line((left,top,left,bottom,right,bottom),fill=v.MUTED,width=3)
  maxT,minT=32,22
  for T in [22,27,32]:
   y=bottom-(T-22)/10*510;d.text((210,y),str(T),font=v.font(28),fill=v.MUTED,anchor='rm')
  for sec in [0,2,4,6]:d.text((left+sec/6*1400,820),str(sec),font=v.font(28),fill=v.MUTED,anchor='mm')
  for m,col in zip(v.materials,['#8bbce0','#dfbc8d']):
   pts=[];upto=max(.05,min(6,(t-69)*1.05))
   for i in range(241):
    sec=i/40
    if sec>upto:break
    T=32 if sec==0 else 32+(m['Tc']-32)*math.erfc(.00015/(2*math.sqrt(1.1e-7*sec)))
    pts.append((left+sec/6*1400,bottom-(T-22)/10*510))
   if len(pts)>1:d.line(pts,fill=col,width=5)
   x,y=pts[-1];d.ellipse((x-7,y-7,x+7,y+7),fill=col)
   d.text((1670,450 if m['name']=='木头' else 690),m['name'],font=v.font(30),fill=col,anchor='lm')
  d.text((960,876),'接触时间 / 秒',font=v.font(29),fill=v.MUTED,anchor='mm')
  d.text((960,210),'纵轴：皮肤表面下 0.15 mm 温度 / °C · 理想模型，非测量数据',font=v.font(24),fill=v.MUTED,anchor='mm')
  return im
 if t<101:
  im=blank('不只看导热快慢');d=ImageDraw.Draw(im)
  labels=[('导热系数','热量传导的能力','k'),('密度','单位体积有多少质量','ρ'),('比热容','单位质量升温所需热量','c')]
  reveal=1 if t<81 else 2 if t<85 else 3
  for i,(name,desc,symbol) in enumerate(labels[:reveal]):
   x=430+i*530;d.text((x,335),symbol,font=v.font(94,True),fill=v.GOLD,anchor='mm')
   d.text((x,470),name,font=v.font(44),fill=v.FG,anchor='mm');d.text((x,545),desc,font=v.font(27),fill=v.MUTED,anchor='mm')
   if t>=85:d.line((x,600,960,710),fill='#526477',width=2)
  if t>=85:
   d.text((960,760),'热感受率   e = √(kρc)',font=v.font(54,True),fill=v.FG,anchor='mm')
   d.text((960,860),'理想短时接触的比较量，不是人体感觉评分',font=v.font(27),fill=v.MUTED,anchor='mm')
  return im
 if t<117:
  im=blank('换个方向：材料比手更热');d=ImageDraw.Draw(im)
  for x,label,temp in [(540,'皮肤',32),(1380,'材料',45)]:
   fill='#d4d8d5' if x==540 else '#e59b65'
   d.rounded_rectangle((x-230,300,x+230,680),radius=22,fill=fill)
   d.text((x,750),label,font=v.font(42),fill=v.FG,anchor='mm')
   d.text((x,825),f'初始 {temp} °C（示意）',font=v.font(29),fill=v.MUTED,anchor='mm')
  if t>=106:
   progress=v.ease((t-106)/2);end=1120-330*progress
   d.line((1120,490,end,490),fill=v.GOLD,width=8);d.polygon([(end,490),(end+25,470),(end+25,510)],fill=v.GOLD)
   d.text((960,590),'热量传向手',font=v.font(30),fill=v.FG,anchor='mm')
  d.text((960,900),'仅作动画推演，请勿触摸高温物体',font=v.font(26),fill=v.MUTED,anchor='mm')
  return im
 if t<133:
  im=blank('摸起来更冷，不一定温度更低');d=ImageDraw.Draw(im)
  for i,(s,sub) in enumerate([('初始温度','决定温差'),('材料性质','影响传热'),('皮肤变化','影响触感')]):
   x=400+i*560;d.text((x,405),s,font=v.font(53,True),fill=v.FG,anchor='mm');d.text((x,505),sub,font=v.font(35),fill=v.MUTED,anchor='mm')
   if i<2:d.line((x+170,420,x+385,420),fill=v.GOLD,width=4)
  d.text((960,725),'手能感受冷热，不能代替温度计。',font=v.font(50),fill=v.GOLD,anchor='mm')
  return im
 if t<142:
  im=v.frame(2);d=ImageDraw.Draw(im)
  d.rectangle((0,95,1920,205),fill=v.BG);d.text((960,155),'室温下，比较金属与木制品的触感',font=v.font(50,True),fill=v.FG,anchor='mm')
  d.rectangle((0,825,1920,1080),fill=v.BG)
  d.text((960,870),'观察触感差异 ≠ 证明温度完全相同',font=v.font(36),fill=v.GOLD,anchor='mm')
  return im
 im=blank('温度，为什么决定热量传递的方向？');d=ImageDraw.Draw(im)
 d.text((960,395),'下一期，接着看。',font=v.font(64,True),fill=v.GOLD,anchor='mm')
 d.text((960,640),'我是忆白',font=v.font(46),fill=v.FG,anchor='mm')
 d.text((960,730),'和你一起，让理解发生。',font=v.font(42),fill=v.MUTED,anchor='mm');return im

if __name__=='__main__':
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'ep03-clean.mp4')],stdin=subprocess.PIPE)
 for i in range(157*30):
  im=frame(i/30);p.stdin.write(im.tobytes())
  if i%(30*30)==0:print('Rendered',i//30,flush=True)
 p.stdin.close();assert p.wait()==0
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'ep03-clean.mp4'),'-vf',f"subtitles={R/'captions.srt'}:force_style='FontName=Noto Sans CJK SC,FontSize=17,Outline=1,Shadow=0,Alignment=2,MarginV=15'",'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'ep03-review.mp4')],check=True)
 print('DONE',flush=True)
