from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

class PopupHelper:
    dialog = None

    @classmethod
    def show_popup(cls, title, message):
        if cls.dialog:
            cls.dialog.dismiss()
        cls.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: cls.dialog.dismiss())
            ],
        )
        cls.dialog.open()
