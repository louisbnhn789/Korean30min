"""Validate delivered data and the actual full-dialogue audio duration."""
import json, zipfile, subprocess, tempfile
from pathlib import Path

def validate(root, apk_path=None):
    root=Path(root)
    if apk_path:
        with zipfile.ZipFile(apk_path) as apk:
            assert apk.testzip() is None
            course=json.loads(apk.read('assets/course.json'))
            names=set(apk.namelist())
            read=lambda key:apk.read('assets/audio/'+key+'.mp3')
            check(course,lambda key:'assets/audio/'+key+'.mp3' in names,read)
            dex=[apk.read(n) for n in names if n.endswith('.dex')]
            assert any(b'Design & Dev by Duy nguyen' in d for d in dex)
            assert any(b'H\xe1\xbb\x99i tho\xe1\xba\xa1i' in d for d in dex)
    else:
        course=json.loads((root/'app/src/main/assets/course.json').read_text())
        audio=root/'app/src/main/assets/audio'
        check(course,lambda key:(audio/(key+'.mp3')).exists(),lambda key:(audio/(key+'.mp3')).read_bytes())

def check(course, exists, read):
    assert course['schemaVersion']==3 and course['expansionCount']==1000
    assert len(course['grammar'])==48 and len(course['dialogues'])==16
    assert len(course['grammarSources'])==8
    assert len({x['h'] for x in course['vocabulary']})==len(course['vocabulary'])
    assert [l['id'] for l in course['grammar']]==list(range(1,49))
    assert [d['id'] for d in course['dialogues']]==list(range(1,17))
    for lesson in course['grammar']:
        assert len(lesson['examples'])==2 and len(lesson['quiz'])==2
        for q in lesson['quiz']:
            assert q['answer'] in q['options'] and len(set(q['options']))==3
        if lesson['id']>40:
            assert lesson['source']['url'].startswith('https://') and lesson['source']['reviewed']=='2026-10-06'
    keys=set()
    def walk(o):
        if isinstance(o,dict):
            if 'a' in o:keys.add(o['a'])
            for v in o.values():walk(v)
        elif isinstance(o,list):
            for v in o:walk(v)
    walk(course)
    assert all(exists(key) and len(read(key))>100 for key in keys)
    with tempfile.TemporaryDirectory() as temp:
        for d in course['dialogues']:
            assert len(d['turns'])==4 and [t['speaker'] for t in d['turns']]==['A','B','A','B']
            assert all(t['h'] and t['v'] for t in d['turns'])
            audio=Path(temp)/(d['a']+'.mp3');audio.write_bytes(read(d['a']))
            actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(audio)],text=True))
            assert 10<=actual<=15,(d['title'],actual)
            assert abs(actual-d['durationSeconds'])<0.03
    print('Verified 48 grammar lessons, 8 cited source lessons, 16 complete 10–15s dialogues and',len(keys),'audio references')

if __name__=='__main__':
    import sys
    validate(Path(__file__).parent,sys.argv[1] if len(sys.argv)>1 else None)
