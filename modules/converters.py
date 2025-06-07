import ffmpeg
from modules.logger import log_event, log_error

def convert_to_mp4(input_path, output_path):
    try:
        ffmpeg.input(input_path).output(output_path, vcodec='libx264', acodec='aac').run(overwrite_output=True)
        log_event(f"Converted {input_path} to MP4.")
    except Exception as e:
        log_error(f"MP4 Conversion Failed: {e}")
        raise
