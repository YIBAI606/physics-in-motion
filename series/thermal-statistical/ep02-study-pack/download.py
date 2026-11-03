from pathlib import Path
import json, urllib.request, hashlib
root = Path(__file__).resolve().parent
out = root / 'pdf'
out.mkdir(exist_ok=True)
results=[]
for item in json.loads((root/'sources.json').read_text(encoding='utf-8')):
    try:
        req=urllib.request.Request(item['url'], headers={'User-Agent':'YibaiStudyPack/1.0'})
        with urllib.request.urlopen(req, timeout=180) as response:
            data=response.read()
        if not data.startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF')
        (out/item['file']).write_bytes(data)
        results.append({'file':item['file'],'status':'downloaded','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        print('OK',item['file'],len(data),'bytes')
    except Exception as e:
        results.append({'file':item['file'],'status':'failed','error':str(e)})
        print('FAILED',item['file'],str(e))
(root/'download-status.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
raise SystemExit(1 if any(r['status']=='failed' for r in results) else 0)
