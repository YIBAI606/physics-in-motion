from pathlib import Path
import json
r=Path(__file__).parent
style='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans CJK SC,42,&H00F3F1ED,&H00F3F1ED,&H001F150E,&H001F150E,0,0,0,0,100,100,0,0,1,2,0,2,120,120,25,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def ts(t):return f'0:{int(t)//60:02}:{int(t)%60:02}.00'
blocks=(r/'captions.srt').read_text().strip().split('\n\n')
texts=['\\N'.join(b.splitlines()[2:]) for b in blocks]
for c,text in zip(json.loads((r/'timeline.json').read_text()),texts):style+=f"Dialogue: 0,{ts(c['start'])},{ts(c['end'])},Default,,0,0,0,,{text}\n"
(r/'captions.ass').write_text(style)
