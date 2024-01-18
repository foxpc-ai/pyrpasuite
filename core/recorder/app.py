import tkinter as tk
from tkinter import ttk
from core.recorder.recorder import Recorder


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Event Recorder")
        self.master.geometry("400x300")
        self.master.configure(bg="light grey")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), background="light grey")
        self.master["padx"] = 10
        self.master["pady"] = 10

        # self.recorder = Recorder()

        self.start_button = ttk.Button(
            master, text="Start recording", command=self.start
        )
        self.start_button.pack(pady=10)
        self.master.bind("<Alt-s>", lambda e: self.start())

        self.pause_button = ttk.Button(master, text="Pause", command=self.pause)
        self.pause_button.pack(pady=10)

        self.resume_button = ttk.Button(master, text="Resume", command=self.resume)
        self.resume_button.pack(pady=10)

        self.stop_button = ttk.Button(master, text="Stop recording", command=self.stop)
        self.stop_button.pack(pady=10)
        self.master.bind("<Alt-x>", lambda e: self.stop())

    def start(self):
        self.recorder = Recorder()
        self.recorder.start()

    def pause(self):
        self.recorder.pause()

    def resume(self):
        self.recorder.resume()

    def stop(self):
        self.recorder.stop()
