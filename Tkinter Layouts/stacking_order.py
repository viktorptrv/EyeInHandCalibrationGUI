"""
Widgets are always placed on top of other widgets when they are created, not when they are placed
the first created widget will be at the bottom, while the last one will be on top
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x400')

label1 = ttk.Label(master=window,
                   text='Label 1',
                   background='green')
label2 = ttk.Label(master=window,
                   text='Label 2',
                   background='yellow')
label3 = ttk.Label(master=window,
                   text='Label 3',
                   background='blue')

# lift method to get lebel 1 on top
# label1.lift()
# label1.tkraise()

button1 = ttk.Button(master=window,
                     text='Raise label 1', command=lambda: label1.lift(aboveThis=label2)) # will raise only on top of label2
button2 = ttk.Button(master=window,
                     text='Raise label 2', command=lambda: label2.lift())
button3 = ttk.Button(master=window,
                     text='Raise label 3', command=lambda: label3.lift())

label1.place(x=50, y=100, width=200, height=150)
label2.place(x=150, y=60, width=140, height=100)
label3.place(x=100, y=80, width=300, height=150)

button1.place(rely=1, relx=0.8, anchor='se')
button2.place(rely=1, relx=1, anchor='se')
button3.place(rely=1, relx=0.6, anchor='se')

window.mainloop()