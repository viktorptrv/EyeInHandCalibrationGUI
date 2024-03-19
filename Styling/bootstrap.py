"""
ttkbootstrap creates a theme and applies it to every widget
"""
import tkinter as tk

import ttkbootstrap
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap import *

window = ttkbootstrap.Window(themename='journal')
window.title('ttk bootstrap intro')
window.geometry('400x300')

label = ttk.Label(master=window,
                  text='Label')
label.pack()

button1 = ttk.Button(master=window,
                     text='Button1',
                    bootstyle='danger')
button1.pack(pady=10)

button2 = ttk.Button(master=window,
                     text='Button2',
                     bootstyle='warning')
button2.pack(pady=10)

button3 = ttk.Button(master=window,
                     text='Button3')
button3.pack(pady=10)

window.mainloop()