from flask import *
from pytube import YouTube
from moviepy.editor import *
import os
import json
import data as data 

#Iniciar Server
app = Flask(__name__)

#Ruta Api
@app.route('/json')
def api_route():
   with open('api.json') as json_file:
      data_json = json.load(json_file)
   link = data_json['link']
   convert = convert_video(link)
   return send_file(convert, as_attachment=True)

#Ruta Api_mp3
@app.route('/json_mp3')
def download():
   with open('api.json') as json_file:
      data_json = json.load(json_file)
   link = data_json['link']
   link = data_json['link']
   convert = convert_audio(link)
   return send_file(convert, as_attachment=True)
#Ruta principal

@app .route('/download', methods=['GET','POST'])
def home():
   if request.method == "POST" :
      if request.form['link']: 
         link = request.form['link']
         yt = YouTube(link)
         date = {
         'title' : yt.title, 
         'url' : yt.thumbnail_url,
         'views': yt.views,
         'autor': yt.author,
         'link' : link,
         'duration' : str(round(yt.length/60,2)).replace('.',':'),
         'autor': yt.author,
         'fecha' : str(yt.publish_date).replace('00:00:00','')
         }
         data.create_api(date) #Creando Api.json
         return render_template('download.html', dato = date)      
   return render_template('download.html')


#convertir Descargar audio
def convert_audio(audio):
   yt = YouTube(audio)
   v = yt.streams.get_audio_only().download()
   v_mp3 = v.replace('mp4', 'mp3')
   mp3 = AudioFileClip(v)
   mp3.write_audiofile(mp3.filename.replace('mp4','mp3'))
   os.remove(v)
   return v_mp3

#Descargar video
def convert_video(video):
   yt = YouTube(video)
   v = yt.streams.get_audio_only().download()
   v_mp3 = v.replace('mp4', 'mp3')
   return v
if __name__ == '__main__':
    app.run()

