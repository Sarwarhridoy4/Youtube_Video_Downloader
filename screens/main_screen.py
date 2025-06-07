from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from threading import Thread

from utils.validators import validate_url, fetch_video_info
from services.download_service import download_video
from services.conversion_service import convert_to_mp4
from components.popup import PopupHelper


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.url_input = ""
        self.destination_folder = ""
        self.selected_quality = ""

        # Build UI
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(0.9, None), height=600, pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.title_label = MDLabel(text="YouTube Video Downloader", halign="center", font_style="H5", size_hint_y=None, height=40)
        self.layout.add_widget(self.title_label)

        self.url_input_field = MDTextField(hint_text="Enter YouTube video URL", size_hint_y=None, height=40)
        self.layout.add_widget(self.url_input_field)

        self.quality_button = MDRaisedButton(text="Select Video Quality", on_release=self.open_quality_dropdown, size_hint_y=None, height=40)
        self.layout.add_widget(self.quality_button)

        self.quality_label = MDLabel(text="Select Video Quality", halign="center", size_hint_y=None, height=30)
        self.layout.add_widget(self.quality_label)

        self.select_folder_button = MDRaisedButton(text="Select Destination Folder", on_release=self.select_folder, size_hint_y=None, height=40)
        self.layout.add_widget(self.select_folder_button)

        self.destination_label = MDLabel(text="No folder selected", halign="center", size_hint_y=None, height=30)
        self.layout.add_widget(self.destination_label)

        self.download_button = MDRaisedButton(text="Download", on_release=self.start_download, size_hint_y=None, height=40)
        self.layout.add_widget(self.download_button)

        self.progress_bar = MDProgressBar(value=0, size_hint_y=None, height=20)
        self.layout.add_widget(self.progress_bar)

        self.eta_label = MDLabel(text="ETA: N/A", halign="center", size_hint_y=None, height=30)
        self.layout.add_widget(self.eta_label)

        self.add_widget(self.layout)

        self.menu = None
        self.file_manager = None

    def open_quality_dropdown(self, *args):
        url = self.url_input_field.text.strip()
        if not validate_url(url):
            PopupHelper.show_popup("Error", "Invalid YouTube URL.")
            return

        try:
            video_info = fetch_video_info(url)
        except Exception as e:
            PopupHelper.show_popup("Error", f"Failed to fetch video info:\n{str(e)}")
            return

        quality_options = [
            {"text": "Best Quality (Auto Merge)", "format": "bv*+ba/b"},
            {"text": "Best Quality (Forced Merge)", "format": "bv+ba/b"},
            {"text": "Medium Quality (720p max)", "format": "bestvideo[height<=720]+bestaudio/best"},
            {"text": "Low Quality", "format": "worst"},
        ]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": option["text"],
                "on_release": lambda x=option: self.set_quality(x['format'])
            }
            for option in quality_options
        ]

        if self.menu:
            self.menu.dismiss()

        self.menu = MDDropdownMenu(caller=self.quality_button, items=menu_items, width_mult=4)
        self.menu.open()

    def set_quality(self, quality_id):
        self.selected_quality = quality_id
        self.quality_label.text = f"Selected Quality: {quality_id}"
        if self.menu:
            self.menu.dismiss()

    def select_folder(self, *args):
        if not self.file_manager:
            self.file_manager = MDFileManager(select_path=self.set_destination_folder)
        self.file_manager.show('/')

    def set_destination_folder(self, path):
        self.destination_folder = path
        self.destination_label.text = f"Folder: {path}"
        if self.file_manager:
            self.file_manager.close()

    def start_download(self, *args):
        url = self.url_input_field.text.strip()
        if not (validate_url(url) and self.selected_quality and self.destination_folder):
            PopupHelper.show_popup("Warning", "Please enter valid URL, select quality and destination folder.")
            return

        self.progress_bar.value = 0
        self.eta_label.text = "ETA: N/A"
        self.download_button.disabled = True

        Thread(target=self._download_thread, args=(url, self.selected_quality, self.destination_folder), daemon=True).start()

    def _download_thread(self, url, quality, destination):
        def progress_hook(d):
            Clock.schedule_once(lambda dt: self.update_progress(d))

        try:
            download_video(url, quality, destination, progress_hook)
        except Exception as e:
            Clock.schedule_once(lambda dt: PopupHelper.show_popup("Error", f"Download failed:\n{str(e)}"))
        finally:
            Clock.schedule_once(lambda dt: self.enable_download_button())

    def enable_download_button(self):
        self.download_button.disabled = False

    def update_progress(self, progress_info):
        status = progress_info.get('status', '')
        if status == 'downloading':
            downloaded = progress_info.get('downloaded_bytes', 0)
            total = progress_info.get('total_bytes', 1)
            if total > 0:
                percent = (downloaded / total) * 100
                self.progress_bar.value = percent
            else:
                self.progress_bar.value = 0

            eta = progress_info.get('eta')
            if eta is not None and isinstance(eta, int) and eta >= 0:
                minutes, seconds = divmod(eta, 60)
                eta_str = f"{minutes:02d}:{seconds:02d}"
            else:
                eta_str = "N/A"

            self.eta_label.text = f"ETA: {eta_str}"

        elif status == 'finished':
            self.progress_bar.value = 100
            self.eta_label.text = "ETA: 00:00"
            PopupHelper.show_popup("Success", "Download completed successfully.")

            filename = progress_info.get('filename')
            if filename:
                Thread(target=self._convert_to_mp4_thread, args=(filename,), daemon=True).start()

        elif status == 'error':
            PopupHelper.show_popup("Error", "An error occurred during download.")
            self.progress_bar.value = 0
            self.eta_label.text = "ETA: N/A"

    def _convert_to_mp4_thread(self, filepath):
        output, error = convert_to_mp4(filepath)
        if error:
            Clock.schedule_once(lambda dt: PopupHelper.show_popup("Conversion Error", error))
        else:
            Clock.schedule_once(lambda dt: PopupHelper.show_popup("Conversion Success", f"Converted to MP4:\n{output}"))
