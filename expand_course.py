import json,hashlib
from pathlib import Path
from manufacturing_vocab import entries
from grammar_content import parse,ZH,KO
try:
 from pypinyin import lazy_pinyin,Style
except ImportError:
 lazy_pinyin=None

def aid(s):return hashlib.sha256(s.encode()).hexdigest()[:16]
def expand(root,lang):
 root=Path(root);file=root/'app/src/main/assets/course.json';course=json.loads(file.read_text())
 original={x['h'] for w in course['weeks'] for x in w['words']}
 seen=set(original);added=[]
 for item in entries(lang):
  if item['h'] in seen:continue
  seen.add(item['h']);item['a']=aid(item['h']);item['p']=' '.join(lazy_pinyin(item['h'],style=Style.TONE)) if lang=='zh' and lazy_pinyin else ''
  added.append(item)
  if len(added)==1000:break
 assert len(added)==1000 and len({x['h'] for x in added})==1000
 # Preserve the original daily schedule, while exposing all learned and extra words in the bank.
 original_items=[];seen=set()
 for wi,w in enumerate(course['weeks']):
  for item in w['words']:
   if item['h'] in seen:continue
   seen.add(item['h']);original_items.append(dict(item,category='Lộ trình · '+w['title'],kind='course'))
 grammar=parse(ZH if lang=='zh' else KO)
 assert len(grammar)==40
 for lesson in grammar:
  for example in lesson['examples']:
   example['a']=aid(example['h']);example['p']=' '.join(lazy_pinyin(example['h'],style=Style.TONE)) if lang=='zh' and lazy_pinyin else ''
 for day in course['days']:
  intro=7 if lang=='zh' else 14
  if day['day']>intro:day['grammarId']=min(40,(day['day']-intro-1)*40//(182-intro)+1)
 course.update(vocabulary=original_items+added,grammar=grammar,expansionCount=len(added),schemaVersion=2)
 assert all(len(l['quiz'])==2 and len(l['examples'])==2 for l in grammar)
 for lesson in grammar:
  for question in lesson['quiz']:
   assert len(set(question['options']))==3 and question['answer'] in question['options']
 assert not (original & {x['h'] for x in added})
 file.write_text(json.dumps(course,ensure_ascii=False,indent=2))
 print(root.name,':',len(original_items),'original +',len(added),'extra; 40 grammar lessons / 80 exercises')
if __name__=='__main__':
 root=Path(__file__).resolve().parent
 lang='zh' if root.name=='ChineseLouis' else 'ko'
 expand(root,lang)
