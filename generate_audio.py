"""Generate Korean audio at BUILD time; the installed app has no network permission."""
import json,time,random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from gtts import gTTS
root=Path(__file__).parent/'app/src/main/assets'
course=json.loads((root/'course.json').read_text())
items={i['a']:i['h'] for w in course['weeks'] for i in [*w['words'],w['sentence']]}
items.update({d['drill']['a']:d['drill']['h'] for d in course['days'] if 'drill' in d})
items.update({i['a']:i['h'] for i in course.get('vocabulary',[])})
items.update({i['a']:i['h'] for lesson in course.get('grammar',[]) for i in lesson['examples']})
out=root/'audio';out.mkdir(exist_ok=True)
def generate(pair):
    key,text=pair;path=out/(key+'.mp3')
    if path.exists() and path.stat().st_size>100: return
    for attempt in range(6):
        try:
            temp=path.with_suffix('.tmp')
            gTTS(text=text,lang='ko',slow=True,timeout=(15,45)).save(str(temp))
            assert temp.stat().st_size>100
            temp.replace(path);return
        except Exception:
            if attempt==5: raise
            time.sleep(2**attempt+random.random())
with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(generate,items.items()))
assert all((out/(key+'.mp3')).stat().st_size>100 for key in items)
print('Validated all',len(items),'offline audio files')
