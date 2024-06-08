from flask import *
from pytube import YouTube
from moviepy.editor import *
import os
import data as data 
#Iniciar Server
app = Flask(__name__)

@app.route('/json', methods=['GET','POST'])
def api_route():
   return send_file('api.json')

@app.route('/download', methods=["GET","POST"])
def home():
   if request.method == "POST":
         if request.form['audio']:
            link_mp3 = request.form['audio']
            convert_link = convert_audio(link_mp3)
            return convert_link
         if request.form['video'] :
            link_mp4 = request.form['video']
            convert_link = convert_video(link_mp4)
            return convert_link
   return render_template('download.html')

# Descargar en formato mp3
def download_audio(link_audio):
      yt = YouTube(link_audio)
      v = yt.streams.get_audio_only().download()
      v_mp3 = v.replace('mp4','mp3')
      audio = AudioFileClip(v)
      audio.write_audiofile(audio.filename.replace('mp4','mp3'))
      #convertir video antes que el usuario lo descargue
      #os.remove(v)
      #return send_file(v_mp3,as_attachment=True)
   
#Descargar en formato mp4
def download_video(link_video): 
   yt = YouTube(link_video)
   v = yt.streams.first().download()
   return send_file(v, as_attachment=True)   

#convertir video
def convert_video(video):
   yt = YouTube(video)
   date = {
      'title' : f"Titulo : {yt.title}", 
      'url' : yt.thumbnail_url,
      'views': yt.views,
      'duration' : yt.length
      }
   return render_template('download.html', dato_mp4 = date)  
            
#convertir audio
def convert_audio(audio):
   yt = YouTube(audio)
   date = {
      'title' : yt.title, 
      'url' : yt.thumbnail_url,
      'views': yt.views,
      'duration' : yt.length
      }
   return render_template('download.html', dato_mp3 = date)  
if __name__ == '__main__':
    app.run()

