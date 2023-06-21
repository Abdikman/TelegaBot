from pytube import YouTube
from pytube.exceptions import RegexMatchError

def upload_video(link, last, second, user_id, data):
    try:
        yt = YouTube(link)
        yt.title = '_'.join(yt.title.split())
        out_path = rf'Video\{last}_{second}_{user_id}_{data.split()[0]}'

        video = yt.streams.filter(progressive=True, file_extension='mp4')
        video = video.order_by('resolution').desc().first()
        return video.download(output_path=out_path)
    except RegexMatchError:
        return 'Error'
