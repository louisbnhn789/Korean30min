package com.louis.korean;

import android.Manifest;
import android.app.*;
import android.os.*;
import android.content.*;
import android.content.pm.PackageManager;
import android.graphics.*;
import android.media.*;
import android.view.*;
import android.widget.*;
import org.json.*;
import java.io.*;
import java.util.*;

public class MainActivity extends Activity {
    JSONObject course; JSONArray weeks, days; LinearLayout body;
    android.content.SharedPreferences prefs;
    MediaPlayer player; MediaRecorder recorder; File recording;
    int currentDay=1, q=0, score=0; boolean answered=false;
    ArrayList<JSONObject> quizItems; boolean listening;
    final int ink=Color.rgb(26,45,63), green=Color.rgb(12,112,101);
    TextView timerLabel; long timerEnd; boolean ticking=false;
    final Handler handler=new Handler(Looper.getMainLooper());
    final Runnable tick=new Runnable(){ public void run(){
        if(!ticking)return;
        long remaining=Math.max(0,(timerEnd-SystemClock.elapsedRealtime())/1000);
        if(timerLabel!=null)timerLabel.setText(String.format(Locale.ROOT,"%02d:%02d",remaining/60,remaining%60));
        if(remaining==0){ticking=false;toast("Đã hết thời gian. Bạn có thể tiếp tục bài học.");}else handler.postDelayed(this,500);
    }};
    @Override public void onCreate(Bundle state){
        super.onCreate(state);
        getWindow().setStatusBarColor(ink); getWindow().setNavigationBarColor(ink);
        // Android 15 edge-to-edge: keep native controls clear of system bars.
        getWindow().getDecorView().setOnApplyWindowInsetsListener((v,insets)->{
            v.setPadding(insets.getSystemWindowInsetLeft(),insets.getSystemWindowInsetTop(),insets.getSystemWindowInsetRight(),insets.getSystemWindowInsetBottom());return insets;
        });
        prefs=getSharedPreferences("progress",MODE_PRIVATE);
        try(InputStream in=getAssets().open("course.json")){
            ByteArrayOutputStream bytes=new ByteArrayOutputStream();byte[] buffer=new byte[4096];int n;while((n=in.read(buffer))!=-1)bytes.write(buffer,0,n);
            course=new JSONObject(bytes.toString("UTF-8"));
            weeks=course.getJSONArray("weeks"); days=course.getJSONArray("days");
        }catch(Exception e){new AlertDialog.Builder(this).setMessage("Không đọc được bài học: "+e.getMessage()).show();return;}
        if(state!=null)currentDay=state.getInt("day",1);
        home();
    }
    String str(JSONObject o,String k){return o.optString(k);}
    JSONObject week(int day){return weeks.optJSONObject((day-1)/7);}
    int dp(int v){return (int)(v*getResources().getDisplayMetrics().density);}
    void screen(String title){
        stopMedia(); stopRecorder(); ticking=false; handler.removeCallbacks(tick); timerLabel=null;
        ScrollView scroll=new ScrollView(this); scroll.setFillViewport(true);scroll.setBackgroundColor(Color.rgb(246,248,246));
        body=new LinearLayout(this);body.setOrientation(LinearLayout.VERTICAL);body.setPadding(dp(18),dp(18),dp(18),dp(24));
        scroll.addView(body);setContentView(scroll);text(title,26,true);
    }
    TextView text(String s,int size,boolean bold){
        TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(ink);t.setPadding(0,dp(6),0,dp(6));
        if(bold)t.setTypeface(null,Typeface.BOLD);body.addView(t);return t;
    }
    void button(String s,Runnable r){
        Button b=new Button(this);b.setText(s);b.setAllCaps(false);b.setTextColor(green);b.setTextSize(16);
        body.addView(b,new LinearLayout.LayoutParams(-1,-2));b.setOnClickListener(v->r.run());
    }
    void toast(String s){Toast.makeText(this,s,Toast.LENGTH_LONG).show();}
    void home(){
        screen("Korean30min · 한국어");
        int done=0;for(int i=1;i<=182;i++)if(prefs.getBoolean("done"+i,false))done++;
        text("Từ số 0 · 26 tuần · 30 phút/ngày",17,false);
        text("Đã hoàn thành "+done+" / 182 ngày",19,true);
        ProgressBar p=new ProgressBar(this,null,android.R.attr.progressBarStyleHorizontal);p.setMax(182);p.setProgress(done);body.addView(p);
        int next=1;while(next<182&&prefs.getBoolean("done"+next,false))next++;
        final int start=next;button("Tiếp tục ngày "+next,()->lesson(start));
        button("Ôn từ cần nhớ",this::review);
        button("Cách học và quyền riêng tư",this::help);
        text("Chọn tuần học",22,true);
        for(int i=0;i<26;i++){final int w=i;int completed=0;for(int d=i*7+1;d<=i*7+7;d++)if(prefs.getBoolean("done"+d,false))completed++;
            button("Tuần "+(i+1)+" · "+str(weeks.optJSONObject(i),"title")+" ("+completed+"/7)",()->weekMenu(w));}
    }
    void weekMenu(int w){
        screen("Tuần "+(w+1)+" · "+str(weeks.optJSONObject(w),"title"));
        button("← Trang chính",this::home);
        for(int d=w*7+1;d<=w*7+7;d++){final int day=d;JSONObject o=days.optJSONObject(d-1);
            button((prefs.getBoolean("done"+d,false)?"✓ ":"")+"Ngày "+d+": "+str(o,"title"),()->lesson(day));}
    }
    void lesson(int day){
        currentDay=day;JSONObject wk=week(day), d=days.optJSONObject(day-1);int phase=d.optInt("phase");
        screen("Ngày "+day+" · "+str(d,"title"));button("← Danh sách tuần",()->weekMenu((day-1)/7));
        text(str(wk,"title"),21,true);
        timerLabel=text("30:00",24,true);
        button("Bắt đầu / bắt đầu lại 30 phút",()->{handler.removeCallbacks(tick);timerEnd=SystemClock.elapsedRealtime()+30*60*1000L;ticking=true;handler.post(tick);});
        JSONArray tasks=course.optJSONArray("tasks").optJSONArray(phase);int[] minutes={5,10,8,5,2};
        for(int i=0;i<5;i++)text(minutes[i]+" phút · "+tasks.optString(i),16,false);
        text("Ghi chú ngôn ngữ",20,true);text(str(wk,"note"),17,false);
        JSONObject drill=d.optJSONObject("drill");if(drill!=null){text("Hangul · luyện âm hôm nay",20,true);text(str(drill,"glyph"),26,true);text(str(drill,"v"),17,false);button("▶ Nghe bài luyện âm",()->play(drill));text(str(drill,"p"),16,false);}
        text("Từ vựng · chạm để nghe",20,true);
        JSONArray words=wk.optJSONArray("words");int start=phase==0||phase==1?0:phase==2?6:0;int end=phase==0||phase==1?6:12;
        for(int i=start;i<end;i++){final JSONObject item=words.optJSONObject(i);button(str(item,"h")+"  "+str(item,"p")+"\n"+str(item,"v"),()->play(item));
            button("Luyện viết "+str(item,"h"),()->writing(item,day));}
        JSONObject sent=wk.optJSONObject("sentence");text("Mẫu câu",20,true);text(str(sent,"h"),25,true);text(str(sent,"p"),17,false);text(str(sent,"v"),17,false);
        button("▶ Nghe mẫu câu",()->play(sent));
        button("🎙 Ghi âm / dừng ghi âm",this::toggleRecord);
        button("▶ Nghe bản ghi của mình",this::playRecording);
        text("Tự so sánh với mẫu: nguyên âm, phụ âm cuối, nối âm, nhịp câu. Ứng dụng chưa chấm phát âm tự động.",15,false);
        button("Kiểm tra đọc · 12 câu",()->startQuiz(false));
        button("Kiểm tra nghe · 12 câu",()->startQuiz(true));
        text("Điểm cao nhất: đọc "+prefs.getInt("read"+day,0)+"/12 · nghe "+prefs.getInt("listen"+day,0)+"/12",16,false);
        button(prefs.getBoolean("done"+day,false)?"✓ Ngày này đã hoàn thành":"Đánh dấu hoàn thành ngày",()->{prefs.edit().putBoolean("done"+day,true).apply();toast("Đã lưu tiến độ");if(day<182)lesson(day+1);else home();});
        button("Học ngày tiếp theo",()->{if(day<182)lesson(day+1);});
    }
    void play(JSONObject item){
        stopMedia();String path="audio/"+str(item,"a")+".mp3";
        try(android.content.res.AssetFileDescriptor fd=getAssets().openFd(path)){
            player=new MediaPlayer();player.setDataSource(fd.getFileDescriptor(),fd.getStartOffset(),fd.getLength());player.prepare();player.start();
            player.setOnCompletionListener(mp->stopMedia());
        }catch(Exception e){stopMedia();toast("Không mở được âm thanh. Hãy dùng APK có đầy đủ audio.");}
    }
    void stopMedia(){if(player!=null){player.release();player=null;}}
    void toggleRecord(){
        if(recorder!=null){stopRecorder();toast("Đã lưu bản ghi trên điện thoại");return;}
        if(checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED){requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},1);return;}
        stopMedia();recording=new File(getFilesDir(),"practice.m4a");
        try{
            recorder=new MediaRecorder();recorder.setAudioSource(MediaRecorder.AudioSource.MIC);recorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AAC);recorder.setOutputFile(recording.getAbsolutePath());recorder.prepare();recorder.start();toast("Đang ghi âm. Chạm lại để dừng (tối đa 90 giây).");
            handler.postDelayed(recordStop,90000);
        }catch(Exception e){stopRecorder();toast("Không ghi được âm thanh. Kiểm tra quyền micro.");}
    }
    final Runnable recordStop=()->{if(recorder!=null){stopRecorder();toast("Đã dừng ghi âm sau 90 giây");}};
    void stopRecorder(){handler.removeCallbacks(recordStop);if(recorder!=null){try{recorder.stop();}catch(RuntimeException e){if(recording!=null)recording.delete();}recorder.release();recorder=null;}}
    void playRecording(){stopRecorder();stopMedia();File f=new File(getFilesDir(),"practice.m4a");if(!f.exists()){toast("Bạn chưa có bản ghi. Hãy ghi âm trước.");return;}
        try{player=new MediaPlayer();player.setDataSource(f.getAbsolutePath());player.prepare();player.start();player.setOnCompletionListener(mp->stopMedia());}catch(Exception e){stopMedia();toast("Bản ghi quá ngắn hoặc không hợp lệ. Hãy ghi lại.");}}
    @Override public void onRequestPermissionsResult(int r,String[] p,int[] g){super.onRequestPermissionsResult(r,p,g);if(r==1&&g.length>0&&g[0]==PackageManager.PERMISSION_GRANTED)toggleRecord();else toast("Bạn vẫn học được các phần khác khi không cấp quyền micro.");}
    void startQuiz(boolean listen){
        listening=listen;quizItems=new ArrayList<>();
        // Weekly checkpoints include the past four weeks; final checkpoint covers the whole course.
        int w=(currentDay-1)/7;int first=(currentDay%7==0)?(w==25?2:Math.max(w>=2?2:0,w-3)):w;
        for(int k=first;k<=w;k++){JSONArray a=weeks.optJSONObject(k).optJSONArray("words");for(int i=0;i<a.length();i++){JSONObject item=a.optJSONObject(i);try{item.put("topic",str(weeks.optJSONObject(k),"title"));}catch(JSONException ignored){}quizItems.add(item);}}
        Collections.shuffle(quizItems);quizItems=new ArrayList<>(quizItems.subList(0,12));q=0;score=0;question();
    }
    void question(){
        screen((listening?"Kiểm tra nghe":"Kiểm tra đọc")+" · "+(q+1)+"/12");
        if(q>=12){result();return;}answered=false;JSONObject item=quizItems.get(q);
        if(listening){text("Nghe rồi chọn nghĩa tiếng Việt.",18,false);button("▶ Nghe / nghe lại",()->play(item));}
        else{text("Chủ đề: "+str(item,"topic"),16,false);text(str(item,"h"),38,true);text("Chọn nghĩa tiếng Việt (gợi âm hiện sau khi trả lời).",16,false);}
        ArrayList<String> options=new ArrayList<>();options.add(str(item,"v"));
        ArrayList<String> pool=new ArrayList<>();for(int w=0;w<weeks.length();w++){JSONArray a=weeks.optJSONObject(w).optJSONArray("words");for(int i=0;i<a.length();i++)pool.add(str(a.optJSONObject(i),"v"));}
        Collections.shuffle(pool);for(String v:pool)if(!options.contains(v)){options.add(v);if(options.size()==4)break;}Collections.shuffle(options);
        TextView feedback=text("",17,false);
        for(String option:options)button(option,()->{
            if(answered)return;answered=true;boolean ok=option.equals(str(item,"v"));if(ok)score++;
            feedback.setText((ok?"✓ Đúng":"Chưa đúng")+" · "+str(item,"h")+" / "+str(item,"p")+" / "+str(item,"v"));
            prefs.edit().putBoolean("weak"+str(item,"a"),!ok).apply();
        });
        button("Câu tiếp theo",()->{if(!answered){toast("Hãy chọn một đáp án trước");return;}q++;if(q==12)result();else question();});
        button("Thoát kiểm tra",()->new AlertDialog.Builder(this).setMessage("Thoát sẽ bỏ kết quả lần này.").setPositiveButton("Thoát",(a,b)->lesson(currentDay)).setNegativeButton("Tiếp tục",null).show());
    }
    void result(){
        screen("Kết quả: "+score+"/12");String key=(listening?"listen":"read")+currentDay;prefs.edit().putInt(key,Math.max(score,prefs.getInt(key,0))).apply();
        text(score>=10?"Bạn đã nhớ khá tốt. Hãy nói lại mẫu câu không nhìn chữ.":"Hãy ôn các từ chưa nhớ và làm lại bài kiểm tra.",19,false);
        text("Đây là kiểm tra tự luyện, không phải chứng chỉ TOPIK. Điểm cao nhất được lưu trên máy.",16,false);
        button("Ôn từ cần nhớ",this::review);button("Về ngày học",()->lesson(currentDay));
    }
    void review(){
        screen("Ôn từ cần nhớ");button("← Trang chính",this::home);int count=0;
        for(int w=0;w<weeks.length();w++){JSONArray a=weeks.optJSONObject(w).optJSONArray("words");for(int i=0;i<a.length();i++){JSONObject item=a.optJSONObject(i);
            if(prefs.getBoolean("weak"+str(item,"a"),false)){count++;button(str(item,"h")+" · "+str(item,"p")+" · "+str(item,"v"),()->play(item));button("Tôi đã nhớ "+str(item,"h"),()->{prefs.edit().putBoolean("weak"+str(item,"a"),false).apply();review();});}}}
        if(count==0)text("Chưa có từ sai cần ôn. Hãy làm bài kiểm tra ở ngày học.",18,false);
    }
    void writing(JSONObject item,int day){
        screen("Luyện viết · "+str(item,"h"));text(str(item,"p")+" · "+str(item,"v"),19,false);
        text("Viết theo hình chữ mờ. Ô này luyện hình dạng, chưa hướng dẫn thứ tự nét hoặc chấm viết tự động. Từ dài: luyện từng khối âm tiết.",16,false);
        Pad pad=new Pad(this,str(item,"h").substring(0,1));body.addView(pad,new LinearLayout.LayoutParams(-1,dp(310)));
        text("Chọn khối âm tiết để luyện. Viết phụ âm đầu, nguyên âm, rồi phụ âm cuối nếu có.",16,false);
        LinkedHashSet<String> syllables=new LinkedHashSet<>();for(char ch:str(item,"h").toCharArray())if(!Character.isWhitespace(ch))syllables.add(String.valueOf(ch));
        for(String syllable:syllables)button("Viết "+syllable,()->{pad.glyph=syllable;pad.clear();});button("Xóa nét vừa viết",pad::clear);button("▶ Nghe",()->play(item));button("← Về bài học",()->lesson(day));
    }
    class Pad extends View {
        Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG);Path path=new Path();String glyph;
        Pad(Context c,String s){super(c);glyph=s;setLayerType(View.LAYER_TYPE_SOFTWARE,null);}
        void clear(){path.reset();invalidate();}
        @Override protected void onDraw(Canvas c){super.onDraw(c);c.drawColor(Color.WHITE);paint.setColor(Color.LTGRAY);paint.setStrokeWidth(dp(1));paint.setStyle(Paint.Style.STROKE);
            c.drawRect(1,1,getWidth()-1,getHeight()-1,paint);c.drawLine(0,getHeight()/2f,getWidth(),getHeight()/2f,paint);c.drawLine(getWidth()/2f,0,getWidth()/2f,getHeight(),paint);
            paint.setStyle(Paint.Style.FILL);paint.setColor(Color.rgb(215,225,220));paint.setTextAlign(Paint.Align.CENTER);paint.setTextSize(Math.min(getHeight()*.55f,getWidth()*.8f/Math.max(1,glyph.length())));
            c.drawText(glyph,getWidth()/2f,getHeight()/2f-(paint.ascent()+paint.descent())/2,paint);
            paint.setColor(green);paint.setStyle(Paint.Style.STROKE);paint.setStrokeWidth(dp(5));paint.setStrokeCap(Paint.Cap.ROUND);paint.setStrokeJoin(Paint.Join.ROUND);c.drawPath(path,paint);
        }
        @Override public boolean onTouchEvent(android.view.MotionEvent e){getParent().requestDisallowInterceptTouchEvent(true);if(e.getAction()==MotionEvent.ACTION_DOWN)path.moveTo(e.getX(),e.getY());else if(e.getAction()==MotionEvent.ACTION_MOVE)path.lineTo(e.getX(),e.getY());else if(e.getAction()==MotionEvent.ACTION_UP)performClick();invalidate();return true;}
        @Override public boolean performClick(){super.performClick();return true;}
    }
    void help(){screen("Cách học Korean30min");
        text("Học liên tục 182 ngày (26 tuần). Mỗi ngày: ôn 5 phút, học mới 10 phút, nghe 8 phút, tự nói/ghi âm 5 phút, đọc/viết 2 phút. Bạn có thể mở bất kỳ ngày nào.",18,false);
        text("Hai tuần đầu học Hangul; các tuần sau học giao tiếp trong công ty điện tử. Đọc ghi chú trước, nghe mẫu, nhắc lại, thay thông tin bằng thông tin thật của bạn.",18,false);
        text("Nghe và bài học dùng dữ liệu đóng gói trong APK, không cần Internet. Micro chỉ dùng khi ghi âm; bản ghi mới thay bản ghi trước. Tiến độ, điểm và bản ghi chỉ nằm trên điện thoại; gỡ ứng dụng sẽ xóa chúng.",18,false);
        text("Audio là giọng Hàn tổng hợp để tự luyện. Nội dung tự biên soạn cho công ty điện tử. Gợi âm bằng chữ Latin chỉ để tham khảo; hãy ưu tiên nghe mẫu và đọc Hangul. Ứng dụng không tự chấm phát âm hay thứ tự nét.",18,false);
        button("Xóa bản ghi âm",()->{stopMedia();new File(getFilesDir(),"practice.m4a").delete();toast("Đã xóa bản ghi");});
        button("Đặt lại toàn bộ tiến độ",()->new AlertDialog.Builder(this).setMessage("Xóa ngày đã học, điểm và danh sách từ sai?").setPositiveButton("Xóa",(a,b)->{prefs.edit().clear().apply();home();}).setNegativeButton("Hủy",null).show());button("← Trang chính",this::home);
    }
    @Override protected void onPause(){super.onPause();stopMedia();stopRecorder();}
    @Override protected void onDestroy(){super.onDestroy();handler.removeCallbacksAndMessages(null);stopMedia();stopRecorder();}
    @Override protected void onSaveInstanceState(Bundle b){b.putInt("day",currentDay);super.onSaveInstanceState(b);}
    @Override public void onBackPressed(){home();}
}
