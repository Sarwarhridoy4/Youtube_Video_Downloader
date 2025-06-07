from kivy.lang import Builder
from kivymd.app import MDApp
from screens.main_screen import MainScreen

class YouTubeDownloaderApp(MDApp):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    YouTubeDownloaderApp().run()
