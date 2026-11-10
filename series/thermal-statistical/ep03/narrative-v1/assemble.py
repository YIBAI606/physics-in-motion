from pathlib import Path
import subprocess,json,re
P=Path(__file__).parent
parts=[('开头','ep03-opening-v2','opening-30s-review.mp4','captions.srt','voiceover.txt'),('Black与潜热','ep03-narrative-v1','black-review.mp4','black.srt','black-voiceover.txt'),('潜热解释','ep03-theory-v1','latent-review.mp4','latent.srt','latent-voiceover.txt'),('Fourier与预测','ep03-narrative-v1','fourier-review.mp4','fourier.srt','fourier-voiceover.txt'),('温度场与曲线','ep03-core-v1','core-40s-review.mp4','captions.srt','voiceover.txt'),('热感受率','ep03-theory-v1','effusivity-review.mp4','effusivity.srt','effusivity-voiceover.txt'),('条件反转','ep03-return-v1','conditions-review.mp4','conditions.srt','conditions-voiceover.txt'),('实验回扣','ep03-return-v1','return-review.mp4','return.srt','return-voiceover.txt'),('情感结尾','ep03-narrative-v1','ending-review.mp4','ending.srt','ending-voiceover.txt')]
lines=[];chapters=[];offset=0;subs=[];voice=[]
def secs(s):
 h,m,s=s.replace(',','.').split(':');return 3600*int(h)+60*int(m)+float(s)
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
for title,folder,video,srt,txt in parts:
 p=P.parent/folder;file=p/video
 duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(file)]))
 lines.append("file '"+str(file)+"'")
 chapters.append({'title':title,'start':offset,'duration':duration})
 voice.append(title+'\n\n'+(p/txt).read_text())
 for b in (p/srt).read_text().strip().split('\n\n'):
  rows=b.splitlines();a,z=rows[1].split(' --> ');subs.append(f'{len(subs)+1}\n{stamp(secs(a)+offset)} --> {stamp(secs(z)+offset)}\n'+ '\n'.join(rows[2:]))
 offset+=duration
(P/'concat.txt').write_text('\n'.join(lines))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-c','copy','-movflags','+faststart',str(P/'review-assembly.mp4')],check=True)
(P/'full-voiceover.txt').write_text('\n\n'.join(voice));(P/'full-captions.srt').write_text('\n\n'.join(subs));(P/'chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2))
print('Assembly duration',offset)
