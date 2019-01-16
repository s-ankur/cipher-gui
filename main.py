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

    def __init__(self, ):
        self.create_textbox()
        self.create_options()
        tk.mainloop()

    def create_options(self):
        self.options = tk.Toplevel()
        tk.Label(self.options, text='Cipher: ').grid(column=0,row=0)
        self.options.title("Options")
        self.cipher_choice_text = tk.StringVar()
        self.cipher_choice_text.set(AVAILABLE_CIPHERS[0])
        self.cipher_choice = tk.OptionMenu(self.options, self.cipher_choice_text, *AVAILABLE_CIPHERS)
        self.cipher_choice.grid(row=0, column=1)
        tk.Button(self.options, text="Encrypt", command=self.on_encrypt).grid(row=1, column=0)
        tk.Button(self.options, text="Decrypt", command=self.on_decrypt()).grid(row=1, column=1)
        tk.Button(self.options, text="Hack", command=self.on_hack).grid(row=1, column=2)


    def create_textbox(self):
        self.textbox = tk.Tk()

        self.textbox.configure(background='white')
        self.textbox.title("Cipher Gui")
        self.textbox.geometry("800x150")

        self.key_text = tk.StringVar()
        self.key_text.set("Key")
        self.key = tk.Entry(self.textbox, font='Calibri 13', textvariable=self.key_text)
        self.source_text = tk.StringVar()
        self.source_text.set("Plaintext")
        self.source = tk.Entry(self.textbox, font='Calibri 13', textvariable=self.source_text)
        self.target_text = tk.StringVar()
        self.target_text.set("Ciphertext")
        self.target = tk.Entry(self.textbox, font='Calibri 13', textvariable=self.target_text)

        self.key.pack(side=TOP, fill=BOTH, expand=0)
        self.key.configure(background='white')
        self.source.pack(side=LEFT, fill=BOTH, expand=1)
        self.source.bind('<Return>', self.on_encrypt)
        self.source.configure(background='white')
        self.target.pack(side=RIGHT, fill=BOTH, expand=1)
        self.target.bind('<Return>', self.on_decrypt)
        self.target.configure(background='white')

    def get_cipher(self):
        return self.ciphers[self.cipher_choice_text.get()]

    def on_encrypt(self, _='unused'):
        self.target_text.set(self.get_cipher().encrypt(self.source_text.get(), self.key_text.get()))

    def on_decrypt(self, _='unused'):
        self.source_text.set(self.get_cipher().decrypt(self.target_text.get(), self.key_text.get()))

    def on_hack(self, _='unused'):
        self.source_text.set(self.get_cipher().hack(self.target_text.get(), self.key_text.get()))


if __name__ == '__main__':
    CipherGUI()
