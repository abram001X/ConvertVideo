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
         if request.form['audio'] :
            link_mp3 = request.form['audio']
            yt = YouTube(link_mp3)
            date = { 
               'title' : yt.title, 
               'url' : yt.thumbnail_url,
               'views': yt.views,
               'duration' : yt.length
               }
            data.create_api(date)
            return render_template('download.html', dato = date)
         if request.form['video'] :
            link_mp4 = request.form['video']
            download_mp4 = download_video(link_mp4)
            return download_mp4
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
def convert_video(title, img, minutes, views):
   return f"""<h2>{title}<h2> <img src={img}> <p>{minutes}<p> <p>{views}<p>"""

   
if __name__ == '__main__':
    app.run()

