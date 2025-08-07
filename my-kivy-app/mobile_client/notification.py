# notification.py
from plyer import notification

def notify_user(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="StealthClient",
        timeout=5
    )
