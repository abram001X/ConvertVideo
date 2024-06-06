from flask import *
from pytube import YouTube
from moviepy.editor import *
import os
app = Flask(__name__)

@app.route('/download', methods=["GET","POST"])
def home():
   if request.method == "POST":
        video = request.form['video']
        yt = YouTube(video)
        v = yt.streams.get_audio_only().download()
        audio = AudioFileClip(v)
        v_mp3 = audio.write_audiofile(audio.filename.replace('mp4','mp3'))
        ruta_vmp3 = os.path.abspath(v_mp3)
        return send_file(ruta_vmp3,as_attachment=True)
        
    
   return render_template('index.html')


   
    

 
  
if __name__ == '__main__':
    app.run()

