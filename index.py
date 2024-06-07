from flask import *
from pytube import YouTube
from moviepy.editor import *
import os

#Iniciar Server
app = Flask(__name__)

@app.route('/download', methods=["GET","POST"])

def home():
   if request.method == "POST":
         if request.form['audio'] :
            link_mp3 = request.form['audio']
            download_mp3 = download_audio(link_mp3)
            return download_mp3
         
         if request.form['video'] :
            
            link_mp4 = request.form['video']
            download_mp4 = download_video(link_mp4)
            return download_mp4
   return render_template('index.html')

# Descargar en formato mp3
def download_audio(link_audio):
      yt = YouTube(link_audio) 
      v = yt.streams.get_audio_only().download()
      v_mp3 = v.replace('mp4','mp3')
      v_audio = v_mp3
      audio = AudioFileClip(v)
      audio.write_audiofile(audio.filename.replace('mp4','mp3'))
      os.remove(v)
      return send_file(v_mp3,as_attachment=True)
   
#Descargar en formato mp4
def download_video(link_video): 
   yt = YouTube(link_video)
   v = yt.streams.first().download()
   return send_file(v, as_attachment=True)   

if __name__ == '__main__':
    app.run()

