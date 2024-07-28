from pytubefix import YouTube,Search
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=Z5zK2Uy-dq8&list=RDZ5zK2Uy-dq8&start_radio=1"

yt = YouTube(url, on_progress_callback = on_progress)
print(yt.title)

ys = yt.streams.get_audio_only()
ys.download(mp3=True)