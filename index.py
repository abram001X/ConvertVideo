from flask import *
from pytube import YouTube,Search
from moviepy.editor import *
import os
import json

#Iniciar Server
app = Flask(__name__)

#Ruta de busqueda con info
@app.route('/apjsdabram/<url>')
def  search_url(url):
   array = url.split(",")
   yt = download_audio_video(array[0],f'https://www.youtube.com/watch?v={array[1]}')
   return send_file(yt, as_attachment=True)


#Ruta de busqueda
@app.route('/search', methods=['GET','POST'])
def search():
   if request.method == 'POST':
      res = request.form['search']
      result = Search(res)
      obj = result.results
      ob = []  
      for i in range(0,5):
        ob.append(obj[i])
      return render_template('search.html', dato = ob)
   
   return render_template('search.html')

#Ruta principal
@app .route('/', methods=['GET','POST'])
def home():
   if request.method == "POST":
      if request.form['link']: 
         link = request.form['link']
         date = convert_url(link)
         return render_template('download.html', dato = date)  
     
   return render_template('download.html')


#Convert Url
def convert_url(link):
    yt = YouTube(link)
    date = {
         'title' : yt.title, 
         'url' : yt.thumbnail_url,
         'views': yt.views,
         'autor': yt.author,
         'link' : link,
         'duration' : str(round(yt.length/60,2)).replace('.',':'),
         'autor': yt.author,
         'fecha' : str(yt.publish_date).replace('00:00:00',''),
         'video_id' : yt.video_id
         }
    return date

#Descargar audio_video usando YouTube()
def download_audio_video(format,url):
   yt = YouTube(url)
   if format == 'mp4':
      v = yt.streams.get_audio_only().download()
      v_mp3 = v.replace('mp4', 'mp3')
      return v
   if format == 'mp3':
      v = yt.streams.get_audio_only().download()
      v_mp3 = v.replace('mp4', 'mp3')
      mp3 = AudioFileClip(v)
      mp3.write_audiofile(mp3.filename.replace('mp4','mp3'))
      os.remove(v)
      return v_mp3

#Descargar audio_video usando Search
#def download_mp4_mp3(format,url):
   
if __name__ == '__main__':
    app.run(port=5000)
   
