from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.properties import StringProperty
from kivy.clock import Clock
import threading
import os

from modules.utils import validate_url, fetch_video_info
from modules.download_manager import download_video_with_progress
from modules.converters import convert_to_mp4
from modules.logger import log_event, log_error


class MainScreen(Screen):
    url_input = StringProperty("")
    destination_folder = StringProperty("")
    selected_quality = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spinner = None
        self.menu = None
        self.build_ui()

    def build_ui(self):
        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        self.layout.size_hint = (0.9, None)
        self.layout.height = 600
        self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.layout.add_widget(MDLabel(text="YouTube Video Downloader", halign="center", font_style="H5"))
        self.url_input_field = MDTextField(hint_text="Enter YouTube video URL")
        self.layout.add_widget(self.url_input_field)

        self.layout.add_widget(MDRaisedButton(text="Select Quality", on_release=self.open_quality_dropdown))
        self.quality_label = MDLabel(text="Quality: Not selected", halign="center")
        self.layout.add_widget(self.quality_label)

        self.layout.add_widget(MDRaisedButton(text="Select Destination", on_release=self.select_folder))
        self.destination_label = MDLabel(text="Folder: Not selected", halign="center")
        self.layout.add_widget(self.destination_label)

        self.download_button = MDRaisedButton(text="Download", on_release=self.start_download)
        self.layout.add_widget(self.download_button)

        self.progress_bar = MDProgressBar(value=0)
        self.layout.add_widget(self.progress_bar)

        self.eta_label = MDLabel(text="ETA: N/A", halign="center")
        self.layout.add_widget(self.eta_label)

        self.spinner = MDSpinner(size_hint=(None, None), size=(46, 46), pos_hint={"center_x": 0.5}, active=False)
        self.layout.add_widget(self.spinner)

        self.add_widget(self.layout)

    def show_popup(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def open_quality_dropdown(self, *args):
        url = self.url_input_field.text
        if not validate_url(url):
            self.show_popup("Error", "Invalid URL")
            return

        video_info = fetch_video_info(url)  # Optional, not used in dropdown here

        quality_options = [
            {"text": "Best (Auto)", "format": "bv*+ba/b"},
            {"text": "720p max", "format": "bestvideo[height<=720]+bestaudio/best"},
            {"text": "Worst", "format": "worst"}
        ]

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": q["text"],
                "on_release": lambda x=q: self.set_quality(x['format'])
            }
            for q in quality_options
        ]

        self.menu = MDDropdownMenu(caller=self.download_button, items=menu_items, width_mult=4)
        self.menu.open()

    def set_quality(self, quality):
        self.selected_quality = quality
        self.quality_label.text = f"Quality: {quality}"
        if self.menu:
            self.menu.dismiss()

    def select_folder(self, *args):
        self.file_manager = MDFileManager(select_path=self.set_destination_folder)
        self.file_manager.show('/')

    def set_destination_folder(self, path):
        self.destination_folder = path
        self.destination_label.text = f"Folder: {path}"
        self.file_manager.close()

    def start_download(self, *args):
        url = self.url_input_field.text
        if not (validate_url(url) and self.selected_quality and self.destination_folder):
            self.show_popup("Warning", "Please fill all fields properly.")
            return

        self.spinner.active = True
        self.progress_bar.value = 0
        self.eta_label.text = "ETA: N/A"
        threading.Thread(
            target=self._run_download,
            args=(url, self.selected_quality, self.destination_folder),
            daemon=True
        ).start()

    def _run_download(self, url, quality, dest):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percent = (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100
                eta = d.get('eta', 'N/A')
                # Schedule progress updates on main thread
                Clock.schedule_once(lambda dt: self.update_progress(percent, eta))

            elif d['status'] == 'finished':
                # Schedule finish handler on main thread
                Clock.schedule_once(lambda dt: self.on_download_finished(d))

        try:
            download_video_with_progress(url, quality, dest, progress_hook)
        except Exception as e:
            log_error(f"Download failed: {e}")
            Clock.schedule_once(lambda dt: self.show_error_and_stop_spinner(f"Download failed: {e}"))

    def update_progress(self, percent, eta):
        self.progress_bar.value = percent
        self.eta_label.text = f"ETA: {eta}s"

    def on_download_finished(self, d):
        self.progress_bar.value = 100
        downloaded_path = d.get('filename')

        if not downloaded_path.endswith('.mp4'):
            try:
                mp4_path = downloaded_path.rsplit('.', 1)[0] + '.mp4'
                convert_to_mp4(downloaded_path, mp4_path)
                os.remove(downloaded_path)
                self.show_popup("Success", "Download and conversion complete.")
            except Exception as e:
                self.show_popup("Error", f"Conversion failed: {e}")
        else:
            self.show_popup("Success", "Download complete.")

        self.spinner.active = False

    def show_error_and_stop_spinner(self, message):
        self.show_popup("Error", message)
        self.spinner.active = False
        self.progress_bar.value = 0
        self.eta_label.text = "ETA: N/A"