import ffmpeg
import os

def convert_to_mp4(input_path: str):
    if not input_path.lower().endswith('.mp4'):
        output_path = os.path.splitext(input_path)[0] + '.mp4'
        try:
            (
                ffmpeg
                .input(input_path)
                .output(
                    output_path,
                    vcodec='libx264',
                    acodec='aac',
                    strict='experimental',
                    **{'b:a': '192k'}  # Optional: set audio bitrate
                )
                .run(overwrite_output=True)
            )
            return output_path, None
        except ffmpeg.Error as e:
            return None, e.stderr.decode() if e.stderr else str(e)
    else:
        return input_path, None

