from yt_dlp import YoutubeDL

def download_video(url, quality, destination_folder, progress_hook):
    ydl_opts = {
        'format': quality,
        'outtmpl': f'{destination_folder}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
