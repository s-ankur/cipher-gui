#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encrypt Badly
"""
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

AVAILABLE_CIPHERS = ('atbash', 'caesar','vigenere')


class CipherGUI:
    ciphers = {name: __import__(name) for name in AVAILABLE_CIPHERS}

    def __init__(self, ):
        self.create_textbox()
        self.create_options()
        tk.mainloop()

    def create_options(self):
        self.options = tk.Toplevel()
        ttk.Label(self.options, text='Cipher: ').grid(column=0, row=0)
        self.options.title("Options")

        self.cipher_docs_string = tk.StringVar()
        self.cipher_docs = ttk.Label(self.options, textvariable=self.cipher_docs_string, justify=LEFT)
        self.cipher_docs.grid(column=0, row=1, rowspan=2, columnspan=4)
        self.cipher_choice_string = tk.StringVar()
        self.cipher_choice_string.trace('w', self.on_cipher)
        self.cipher_choice_string.set(AVAILABLE_CIPHERS[0])

        self.cipher_choice = tk.OptionMenu(self.options, self.cipher_choice_string, *AVAILABLE_CIPHERS)
        self.cipher_choice.grid(row=0, column=1)
        ttk.Button(self.options, text="Encrypt", command=self.on_encrypt).grid(row=4, column=0)
        ttk.Button(self.options, text="Decrypt", command=self.on_decrypt).grid(row=4, column=1)
        ttk.Button(self.options, text="Hack", command=self.on_crack).grid(row=4, column=2)
        ttk.Button(self.options, text="Clear", command=self.on_clear).grid(row=4, column=3)


    def create_textbox(self):
        self.textbox = tk.Tk()

        self.textbox.configure(background='white')
        self.textbox.title("Cipher Gui")
        self.textbox.geometry("800x150")

        self.key_string = tk.StringVar()
        self.key_string.set("Key")
        self.key = ttk.Entry(self.textbox, font='Calibri 13', textvariable=self.key_string)
        self.plaintext_string = tk.StringVar()
        self.plaintext_string.set("Plaintext")
        self.plaintext = ttk.Entry(self.textbox, font='Calibri 13', textvariable=self.plaintext_string)
        self.ciphertext_string = tk.StringVar()
        self.ciphertext_string.set("Ciphertext")
        self.ciphertext = ttk.Entry(self.textbox, font='Calibri 13', textvariable=self.ciphertext_string)

        self.key.pack(side=TOP, fill=BOTH, expand=0)
        self.key.configure(background='white')
        self.plaintext.pack(side=LEFT, fill=BOTH, expand=1)
        self.plaintext.bind('<Return>', self.on_encrypt)
        self.plaintext.configure(background='white')
        self.ciphertext.pack(side=RIGHT, fill=BOTH, expand=1)
        self.ciphertext.bind('<Return>', self.on_decrypt)
        self.ciphertext.configure(background='white')

    def get_cipher(self):
        return self.ciphers[self.cipher_choice_string.get()]

    def on_cipher(self, *args):
        self.cipher_docs_string.set('\n'.join(textwrap.wrap(self.get_cipher().__doc__, 60)))

    def on_encrypt(self, _='unused'):
        self.ciphertext_string.set(self.get_cipher().encrypt(self.plaintext_string.get(), self.key_string.get()))

    def on_decrypt(self, _='unused'):
        self.plaintext_string.set(self.get_cipher().decrypt(self.ciphertext_string.get(), self.key_string.get()))

    def on_crack(self, _='unused'):
        plaintext, key = self.get_cipher().crack(self.ciphertext_string.get())
        self.plaintext_string.set(plaintext)
        self.key_string.set(key)

    def on_clear(self, _='unused'):
        self.ciphertext_string.set('')
        self.key_string.set('')
        self.plaintext_string.set('')



if __name__ == '__main__':
    CipherGUI()
