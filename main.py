#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encrypt Badly
"""
import tkinter as tk
from tkinter.constants import *

AVAILABLE_CIPHERS = ('atbash', 'caesar')


class CipherGUI:
    ciphers = {name: __import__(name) for name in AVAILABLE_CIPHERS}

    def __init__(self, current='atbash'):
        self.current = current
        self.create_gui()

    def create_gui(self):
        self.window = tk.Tk()
        self.w = tk.Tk()
        self.window.configure(background='white')
        self.window.title("Cipher Gui")
        self.window.geometry("800x150")

        self.source_text = tk.StringVar()
        self.source_text.set("Plaintext")
        self.source = tk.Entry(self.window, font='Calibri 13', textvariable=self.source_text)
        self.target_text = tk.StringVar()
        self.target_text.set("Ciphertext")

        self.target = tk.Entry(self.window, font='Calibri 13', textvariable=self.target_text)

        self.source.pack(side=LEFT, fill=BOTH, expand=1)
        self.source.bind('<Return>', self.on_enter_source)
        self.target.pack(side=RIGHT, fill=BOTH, expand=1)
        self.target.bind('<Return>', self.on_enter_target)
        self.source.configure(background='white')
        self.target.configure(background='white')
        self.window.mainloop()

    def on_enter_source(self, _):
        self.target_text.set(self.ciphers[self.current].encrypt(self.source_text.get()))

    def on_enter_target(self, _):
        self.source_text.set(self.ciphers[self.current].decrypt(self.target_text.get()))


if __name__ == '__main__':
    CipherGUI()
