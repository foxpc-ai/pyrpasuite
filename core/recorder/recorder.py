from pynput import keyboard, mouse
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer
import datetime
import re
from core.auto_web import AutoWeb
from core.auto_sys import AutoSys


class Recorder:
    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.is_paused = False
        self.currently_typed_word = ""
        self.actions_dict = {}

    def get_foreground_window_title(self) -> Optional[str]:
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)

        if buf.value:
            return buf.value
        else:
            return None

    def on_press(self, key):
        if not self.is_paused:
            a = self.get_foreground_window_title()
            try:
                self.currently_typed_word += key.char  # if it's a character key
            except AttributeError:
                if key == keyboard.Key.space or key == keyboard.Key.enter:
                    print(f"Word typed: {self.currently_typed_word} on window {a}")
                    self.actions_dict[
                        "Type " + self.currently_typed_word + " on " + "window " + a
                    ] = datetime.datetime.now()
                    self.currently_typed_word = ""
                    print(self.actions_dict)

    # def on_release(self, key):
    #     if not self.is_paused:
    #         a = self.getForegroundWindowTitle()
    #         print(f"Key released: {key} on windows {a}")

    # def on_move(self, x, y):
    #     print(f"Mouse moved to ({x}, {y})")

    def on_click(self, x, y, button, pressed):
        if not self.is_paused:
            a = self.get_foreground_window_title()
            self.actions_dict[
                "click cordinates " + str(x) + str(y) + " on window " + a
            ] = datetime.datetime.now()
            # print(f"Mouse {'pressed' if pressed else 'released'} at ({x}, {y}) on windows {a}")

    # def on_scroll(self, x, y, dx, dy):
    #     print(f"Mouse scrolled at ({x}, {y})")

    def start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.parser()

    def parser(self):
        web = AutoWeb()
        syst = AutoSys()
        browser_list = ["chrome", "firefox"]
        action_list = self.actions_dict
        pattern = r"- (.*)$"
        try:
            for key in action_list.keys():
                a = re.search(pattern, key)
                if a:
                    b = a.group(1)
                    if b.lower() in browser_list:
                        web.open_browser(b)
                        print(b)
                        print("browser")
                    else:
                        syst.open_application(b)
                        print(b)
                        print("application")
        except Exception as e:
            print(e)
