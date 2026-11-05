from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess,json,zipfile
R=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
BG='#101722'; WHITE='#eef3fa'; MUTED='#a6b5c9'; ORANGE='#ffb45e'; BLUE='#64baff'; GREEN='#7be0bd'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)
def frame(t,vertical):
 w,h=(540,960) if vertical else (960,540)
 im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im)
 def txt(x,y,s,size=22,col=WHITE,anchor='mm',bold=False):d.text((x,y),s,font=font(size,bold),fill=col,anchor=anchor)
 # Start with result, rewind to equal-size comparison, then enlarge A.
 if vertical:
  growth=1
  title='温度一样，能量能差一倍？'
  subtitle='相同振子 · 比较平均激发能量'
  phase=0 if t<5 else 1 if t<11 else 2
  lines=[['左边的振子数量，是右边的两倍。'],['同温时，每个相同振子的','平均激发能相同。'],['振子数量翻倍，','平均总能量也翻倍。']][phase]
  xs=[155,385]; cy=320; boxw=190; boxh=235; base=715; maxbar=155
  txt(270,58,'不会物理的忆白',18,MUTED)
  txt(270,112,title,29,bold=True);txt(270,145,subtitle,17,MUTED)
 else:
  growth=1 if t<7 else (0 if t<12 else ease((t-12)/5))
  title='温度一样，平均能量却不同？' if t<7 else '如果把左边扩大一倍呢？'
  subtitle='相同振子 · 比较平均激发能量'
  lines= ['它们可以处于同样的温度。'] if t<7 else ['先从两个同样大小的系统开始。'] if t<12 else ['保持温度不变，把左边的振子数量增加一倍。'] if t<19 else ['温度相同，不要求总能量相同。']
  xs=[280,680];cy=215;boxw=300;boxh=150;base=436;maxbar=80
  txt(40,28,'不会物理的忆白',17,MUTED,'lm')
  txt(w/2,72,title,32,bold=True);txt(w/2,112,subtitle,17,MUTED)
 for side,x in enumerate(xs):
  color=ORANGE if side==0 else BLUE
  d.rounded_rectangle((x-boxw/2,cy-boxh/2,x+boxw/2,cy+boxh/2),radius=15,outline='#344358',width=2)
  rows,cols=4,3
  spacingx=38 if vertical else 62;spacingy=39 if vertical else 35
  for row in range(rows):
   for col in range(cols):
    extra=row>=2
    opacity=(growth if side==0 else 0) if extra else 1
    if opacity<.01:continue
    px=x+(col-1)*spacingx
    py=cy+(row-1.5)*spacingy
    # Equal visual oscillation amplitude illustrates identical oscillators, not instantaneous energy equality.
    dx=5*math.sin(t*3+row*1.4+col*2+side)
    c=tuple(int(int(color[i:i+2],16)*opacity+int(BG[i:i+2],16)*(1-opacity)) for i in (1,3,5))
    d.line((px-12,py,px+12,py),fill='#40506a',width=2)
    d.ellipse((px+dx-6,py-6,px+dx+6,py+6),fill=c)
  n=round(6*(1+growth)) if side==0 else 6
  txt(x,cy+boxh/2+24,f'{n} 个相同振子',18,color)
  # Fixed, equal-temperature badge.
  txt(x,cy-boxh/2-25,'同一温度 T',19,GREEN)
  value=1+growth if side==0 else 1
  bh=maxbar*value/2
  bw=58 if vertical else 82
  d.rounded_rectangle((x-bw/2,base-bh,x+bw/2,base),radius=5,fill=color)
  label='2E' if value>1.99 else 'E' if value<1.01 else f'{value:.1f}E'
  txt(x,base-bh-20,label,23,color,bold=True)
  txt(x,base+24,'平均总能量',17,MUTED)
 if vertical:
  if 5<=t<11:
   txt(270,488,'每个振子的平均激发能相同',18,GREEN)
  for i,line in enumerate(lines):txt(w/2,825+i*33,line,23,bold=True)
  txt(w/2,922,'图示数量用于说明比例；不表示瞬时分配固定',12,MUTED)
 else:
  txt(w/2,492,lines[0],23,bold=True)
  txt(w-20,h-15,'示意：平均值，不代表每次分配',12,MUTED,'rm')
 return im

def render(name,vertical,duration):
 w,h=(540,960) if vertical else (960,540)
 fps=24
 p=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(R/name)],stdin=subprocess.PIPE)
 for i in range(fps*duration):
  im=frame(i/fps,vertical)
  p.stdin.write(im.tobytes())
  if i in [0,8*fps,18*fps]:im.save(R/f'{Path(name).stem}-{i//fps:02d}s.png')
 p.stdin.close();assert p.wait()==0
 print(name,'complete',flush=True)
if __name__=='__main__':
 render('bilibili-opening.mp4',False,24)
 render('douyin-opening.mp4',True,20)
