from yt_dlp import YoutubeDL
import re

def validate_url(url: str) -> bool:
    # Basic YouTube URL validation (improve as needed)
    regex = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    return re.match(regex, url) is not None

def fetch_video_info(url: str) -> dict:
    ydl_opts = {'quiet': True, 'skip_download': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info
