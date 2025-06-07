import re
import shutil
from yt_dlp import YoutubeDL

def validate_url(url):
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
    return re.match(youtube_regex, url) is not None

def fetch_video_info(url):
    ydl_opts = {'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def check_ffmpeg_installed():
    return shutil.which('ffmpeg') is not None
