from flask import *
from pytube import YouTube
from moviepy.editor import *
import os
import json
import data as data 

#Iniciar Server
app = Flask(__name__)

@app.route('/json')
def api_route():
   with open('api.json') as json_file:
      data_json = json.load(json_file)
   link = data_json['file']
   return send_file(link, as_attachment=True)

@app.route('/json_mp3')
def download():
   with open('api.json') as json_file:
      data_json = json.load(json_file)
   link = data_json['file_mp3']
   return send_file(link, as_attachment=True)

@app.route('/download', methods=["GET","POST"])
def home():
   if request.method == "POST" :
      if request.form['link']: 
         link = request.form['link']
         date = convert_audio(link)
         data.create_api(date)
         return render_template('download.html', dato = date)      
   return render_template('download.html')


#convertir Descargar audio
def convert_audio(audio):
   yt = YouTube(audio)
   v = yt.streams.get_audio_only().download()
   v_mp3 = v.replace('mp4', 'mp3')
   mp3 = AudioFileClip(v)
   mp3.write_audiofile(mp3.filename.replace('mp4','mp3'))
   date = {
         'title' : yt.title, 
         'url' : yt.thumbnail_url,
         'views': yt.views,
         'duration' : yt.length,
         'file' : v,
         'file_mp3' : v_mp3.replace('mp4','mp3')
         }
   return date

if __name__ == '__main__':
    app.run()

