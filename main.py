from kivymd.app import MDApp
from kivy.core.window import Window
from modules.ui_components import MainScreen
from modules.utils import check_ffmpeg_installed
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

Window.size = (360, 640)

class YouTubeDownloaderApp(MDApp):
    def build(self):
        if not check_ffmpeg_installed():
            dialog = MDDialog(
                title="FFmpeg Not Found",
                text="FFmpeg is required for this app to work. Please install it and restart.",
                buttons=[MDRaisedButton(text="Exit", on_release=lambda x: self.stop())]
            )
            dialog.open()
        return MainScreen()

if __name__ == '__main__':
    YouTubeDownloaderApp().run()
