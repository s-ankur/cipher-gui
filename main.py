#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encrypt Badly
"""
import string
import tkinter as tk
from tkinter.constants import *

def encrypt_char(char):
    if char in string.ascii_lowercase:
        return string.ascii_lowercase[-(1+string.ascii_lowercase.index(char))]
    elif char in string.ascii_uppercase:
        return string.ascii_uppercase[-(1+string.ascii_uppercase.index(char))]
    return char

def encrypt(plaintext):
    return ''.join(list(map(encrypt_char,plaintext)))

decrypt = encrypt

class TkinterWindow:

    def __init__(self):
        
        self.window = tk.Tk()
        self.window.configure(background='white')
        self.window.title("Cipher Gui")
        self.window.geometry("800x150")
        self.source_text = tk.StringVar()
        self.source_text.set("Plaintext")
        self.source = tk.Entry(self.window,font='Calibri 13',textvariable=self.source_text)
        self.target_text = tk.StringVar()
        self.target_text.set("Ciphertext")

        self.target = tk.Entry(self.window,font='Calibri 13',textvariable=self.target_text)


        self.source.pack(side = LEFT,fill=BOTH,expand=1)
        self.source.bind('<Return>', self.on_enter_source)
        self.target.pack(side = RIGHT,fill=BOTH,expand=1)
        self.target.bind('<Return>', self.on_enter_target)
        self.source.configure(background='white')
        self.target.configure(background='white')
        self.window.mainloop()

    def on_enter_source(self,_):
        self.target_text.set(encrypt(self.source_text.get()))
        
    def on_enter_target(self,_):
        self.source_text.set(decrypt(self.target_text.get()))
    



TkinterWindow()
