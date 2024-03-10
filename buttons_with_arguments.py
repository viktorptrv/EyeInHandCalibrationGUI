import tkinter as tk
from tkinter import ttk


def button_func(param):
    print(param.get())


window = tk.Tk()
window.geometry('500x800')

entry_string = tk.StringVar(value='test')
entry = ttk.Entry(master=window)
entry.pack()

# Using lambda it tells python to only execute the code when the button is pressed
button = ttk.Button(window,
                    text='button',
                    command=lambda: button_func(entry_string))
button.pack()

window.mainloop()