#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Encrypt Badly: Main Gui
"""
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import test

AVAILABLE_CIPHERS = ('nocipher', 'atbash', 'caesar', 'playfair', 'hill', 'vigenere', 'des')


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
        ttk.Button(self.options, text="Simmons", command=self.on_simmons).grid(row=5, column=0)
        ttk.Button(self.options, text="Avalanche", command=self.on_avalanche).grid(row=5, column=1)
        ttk.Button(self.options, text="Clear", command=self.on_clear).grid(row=5, column=2)

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
        self.plot([1, 123, 1, 132, 231])

    def on_simmons(self, _='unused'):
        freq = test.get_freq(self.ciphertext_string.get())
        self.plot(freq)

    def on_avalanche(self, _='unused'):
        cip = self.get_cipher()
        if cip.cipher_type == 'block':
            result = test.avalanche(cip)['diff']
            self.plot(zip(result, result), max(result))
        else:
            print("Only For Block Ciphers")

    def plot(self, data, max_n=1):
        plot_window = tk.Toplevel()
        data = list(data)
        ma = max(data, key=lambda x: x[1])
        c_width = len(data) * 27
        c_height = 350
        y_stretch = 15
        # gap between lower canvas edge and x axis
        y_gap = 20
        # stretch enough to get all data items in
        x_stretch = 20 * 8 / len(data)
        x_width = 15
        # gap between left canvas edge and y axis
        x_gap = 20
        c = tk.Canvas(plot_window, width=c_width, height=c_height, bg='white')
        c.pack()
        for x, (z, y) in enumerate(data):
            y = y * 10 / ma[1]
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            c.create_rectangle(x0, y0, x1, y1, fill="red")
            c.create_text(x0 + 2, y0, anchor=tk.SW, text=str(z))


if __name__ == '__main__':
    c = CipherGUI()
