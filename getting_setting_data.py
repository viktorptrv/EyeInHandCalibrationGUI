# Config method to update the widget
# label.config(text='new text')
# label['text']='new text'

import tkinter as tk
from tkinter import ttk
import time


def button_func():
    print(entry.get())

    # update the label
    label.config(text='new name')


window = tk.Tk()
window.geometry('700x500')

label = ttk.Label(master=window,
                  text="Label")
label.pack()

entry = ttk.Entry(master=window)
entry.pack()

button = ttk.Button(master=window,
                    text="The Button",
                    command=button_func)
button.pack()

window.mainloop()
