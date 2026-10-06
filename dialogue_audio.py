"""Assemble complete dialogues and measure their actual packaged duration."""
import json, subprocess, tempfile, wave
from pathlib import Path

def duration(path):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True).strip())

def assemble(course, audio, course_file):
    for dialogue in course['dialogues']:
        target=audio/(dialogue['a']+'.mp3')
        if not target.exists() or target.stat().st_size<100:
            with tempfile.TemporaryDirectory() as temp:
                temp=Path(temp); pcm=bytearray()
                for index, turn in enumerate(dialogue['turns']):
                    wav=temp/(str(index)+'.wav')
                    trim='silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse'
                    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(audio/(turn['a']+'.mp3')),'-af',trim,'-ar','24000','-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
                    with wave.open(str(wav),'rb') as w:
                        assert w.getnchannels()==1 and w.getframerate()==24000
                        pcm.extend(w.readframes(w.getnframes()))
                    if index<3:pcm.extend(b'\x00\x00'*4800)  # 0.2 s between speakers
                joined=temp/'joined.wav'
                with wave.open(str(joined),'wb') as w:
                    w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(pcm)
                original_seconds=len(pcm)/(24000*2)
                desired=max(10.7,min(14.3,original_seconds))
                tempo=original_seconds/desired
                assert 0.65<=tempo<=1.5, (dialogue['title'],original_seconds,'Revise the dialogue text instead of cutting speech')
                output=temp/'full.mp3'
                subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(joined),'-af',f'atempo={tempo:.8f}','-c:a','libmp3lame','-b:a','64k',str(output)],check=True)
                assert 10<=duration(output)<=15
                output.replace(target)
        actual=duration(target)
        assert 10<=actual<=15,(dialogue['title'],actual)
        dialogue['durationSeconds']=round(actual,2)
        print('Dialogue',dialogue['id'],dialogue['title'],f'{actual:.2f}s')
    course_file.write_text(json.dumps(course,ensure_ascii=False,indent=2))
