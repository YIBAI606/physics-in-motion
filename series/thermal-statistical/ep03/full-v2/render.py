from pathlib import Path
from PIL import Image,ImageDraw
import json,math,subprocess
import scenes as old
import visual_base as v
R=Path(__file__).parent
# 32 stages, each delivering a new reasoning step, 8 seconds per stage.
texts=[
'一块金属，一块木头，在同一个房间放了很久。它们的温度可以几乎一样。',
'但用手一摸，金属明显更冷。问题来了：一样的温度，为什么会有不同的触感？',
'我们先锁定比较条件：初始温度相同，接触时间相同，再看看手发生了什么。',
'通常，手的皮肤比室温下的物体更暖。两者接触后，热量会从手流向物体。',
'所以，这里并不是物体把某种冷传给了手，而是手正在失去热量。',
'皮肤的降温过程会影响冷的感觉。物体的初始温度相同，皮肤的变化却未必相同。',
'为了看清原因，我们把接触处切开。左边是皮肤，右边是材料内部。',
'两幅图使用相同的温度色阶。相同颜色表示相同温度，虚线标出接触面。',
'先看木头。接触处收到热量之后，不容易很快把这些热量传向更深的内部。',
'于是，温度变化更集中在表面附近。这一小块区域，比内部更容易暖起来。',
'再看金属。热量更容易向内部扩散，温度变化可以影响到更深的区域。',
'这意味着，不只是贴着手的薄薄一层，更多内部材料也能参与吸收热量。',
'在常见条件下，金属因此会让接触附近的皮肤降温更明显，我们就觉得它更冷。',
'接下来，把皮肤温度画成曲线。横轴是接触时间，纵轴是同一皮肤深度的温度。',
'两条曲线从同一个温度出发。蓝线对应接触金属，棕线对应接触木头。',
'看最初一小段：两条线开始分开。接触不同材料，皮肤经历了不同的降温过程。',
'再往后看，金属对应的温度更低。但这不是说，金属在接触前就更冷。',
'这里的曲线来自简化传热模型，不是人体实验数据。它帮助我们分清原因和结果。',
'不过，只说金属导热快，还不够完整。材料升温需要吸收多少热量，也会影响接触过程。',
'同样大小的材料，密度不同，包含的质量就不同。单位体积吸热后的温升也会受影响。',
'即使质量相同，不同材料升高一度所需的热量也可能不同。这个差别由比热容描述。',
'对于理想的短时间接触，可以把导热系数、密度和比热容合在一起，得到热感受率。',
'这个量越大，通常越能在自身表面温度变化较小的情况下，接受或释放热量。',
'因此，比较材料时，需要同时考虑导热和储热。热感受率也不是人体感觉的直接评分。',
'现实接触还有更多条件：表面是否贴合、接触面积多大、材料是否潮湿，都可能改变结果。',
'所以，动画里先让这些条件尽量一致，才能突出材料性质带来的差别。',
'现在把温差反过来。如果金属和木头都比手更热，热量就会从材料传向手。',
'在合适的接触条件下，金属也可能显得更烫。它并不是天生冷，而是会影响热量传递。',
'回到开头：摸起来更冷，不一定温度更低。还要看接触以后，皮肤怎样失去热量。',
'你可以把室温下的金属勺和木制品放置足够久，再比较触感。但触摸不能证明温度完全相同。',
'你的手能感受冷热，却不能仅凭触感准确比较不同材料的温度。下一期，再追问温度的意义。',
'我是忆白，和你一起，让理解发生。'
]
assert len(texts)==32
DURATION=256
cues=[dict(start=i*8,end=(i+1)*8,text=s) for i,s in enumerate(texts)]
def stamp(t):return f'00:{int(t)//60:02}:{int(t)%60:02},000'
def wrap(s,n=28):
 if len(s)<=n:return s
 # Balanced two-line captions where possible; prefer punctuation.
 midpoint=len(s)//2
 choices=[i+1 for i,c in enumerate(s) if c in '，。？：' and len(s)-n<=i+1<=n]
 k=min(choices,key=lambda x:abs(x-midpoint)) if choices else min(n,midpoint)
 return s[:k]+'\n'+s[k:]
assert all(len(wrap(s).splitlines())<=2 and max(map(len,wrap(s).splitlines()))<=28 for s in texts)
(R/'voiceover.txt').write_text('\n\n'.join(texts))
(R/'timeline.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
(R/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{wrap(c['text'])}" for i,c in enumerate(cues))+'\n')
def panel(title,steps,n):
 im=old.blank(title);d=ImageDraw.Draw(im)
 for i,(heading,sub) in enumerate(steps[:n]):
  x=400+i*560
  d.rounded_rectangle((x-210,310,x+210,650),radius=20,outline='#526477',width=3)
  d.text((x,410),heading,font=v.font(46,True),fill=v.GOLD,anchor='mm')
  d.text((x,545),sub,font=v.font(29),fill=v.FG,anchor='mm')
 return im

def frame(t):
 i=min(31,int(t//8));u=t%8
 if i<3:im=old.frame(min(13.9,t*.62))
 elif i<6:
  im=old.blank('手失去热量，皮肤温度下降');d=ImageDraw.Draw(im)
  for x,title,temp,col in [(540,'皮肤','初始较暖','#e59b65'),(1380,'物体','初始较冷','#538dc0')]:
   d.rounded_rectangle((x-220,300,x+220,690),radius=26,fill=col)
   d.text((x,765),title,font=v.font(44),fill=v.FG,anchor='mm');d.text((x,832),temp,font=v.font(30),fill=v.MUTED,anchor='mm')
  tip=810+300*v.ease(u/4);d.line((810,500,tip,500),fill=v.GOLD,width=7)
  d.polygon([(tip,500),(tip-24,480),(tip-24,520)],fill=v.GOLD)
  d.text((960,600),'热量 →',font=v.font(35),fill=v.FG,anchor='mm')
 elif i<13:
  # Rewind explicitly for comparing the same interval, rather than holding a static field.
  local=(t-48) if i<8 else (t-64) if i<10 else (t-80)
  tau=.05+min(6,local*.3)
  im=v.frame(8+tau/.65);d=ImageDraw.Draw(im)
  if 8<=i<10:d.rounded_rectangle((1025,265,1835,820),radius=12,outline=v.GOLD,width=3)
  if 10<=i<13:d.rounded_rectangle((85,265,895,820),radius=12,outline=v.GOLD,width=3)
  d.text((960,913),f'模型重播 · 接触后 {tau:.1f} s · 统一温标 · 非实测',font=v.font(23),fill=v.MUTED,anchor='mm')
 elif i<18:
  # Reveal axes, then grow both curves over 16 seconds, then hold to interpret.
  phase=max(0,min(6,(t-112)/2.65))
  im=old.frame(69+phase/1.05)
  if i==13:
   d=ImageDraw.Draw(im);d.rectangle((245,265,1635,775),fill=v.BG)
   d.text((960,520),'先读坐标，再看曲线',font=v.font(44),fill=v.GOLD,anchor='mm')
 elif i<24:
  q=[78,82,86,90,95,99][i-18]
  im=old.frame(q)
  if i==22:
   d=ImageDraw.Draw(im);d.rectangle((0,815,1920,920),fill=v.BG)
   d.text((960,860),'短时理想接触：同时考虑传热与储热',font=v.font(32),fill=v.MUTED,anchor='mm')
 elif i<26:im=panel('现实接触，条件也重要',[('接触状态','表面是否贴合'),('接触面积','比较时尽量一致'),('含水状态','潮湿会改变传热')],min(3,1+int((t-192)/3)))
 elif i<28:im=old.frame(101+(t-208)*.98)
 elif i==28:im=old.frame(121)
 elif i==29:im=old.frame(138)
 else:im=old.frame(146 if i==30 else 153)
 # A strict shared layout: scene graphics are confined above 918px.
 # The caption band is repainted every frame, so inherited text cannot leak through.
 d=ImageDraw.Draw(im);d.rectangle((0,932,1920,1080),fill=v.BG)
 return im
if __name__=='__main__':
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'ep03-v2-clean.mp4')],stdin=subprocess.PIPE)
 for j in range(DURATION*30):
  im=frame(j/30);p.stdin.write(im.tobytes())
  if j%(30*40)==0:print('Rendered',j//30,flush=True)
 p.stdin.close();assert p.wait()==0
 subprocess.run(['python',str(R/'build_ass.py')],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'ep03-v2-clean.mp4'),'-vf',f"subtitles={R/'captions.ass'}",'-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(R/'ep03-v2-review.mp4')],check=True)
 print('DONE',flush=True)
