import tkinter as tk
from tkinter import ttk

# variables are automatically updated by a widget and they update a widget

window = tk.Tk()
window.geometry('600x300')
window.title('Variables')

# TKinter Variable
# Creating a string variable
# Whatever is written on the entry will be displayed on the label
string_var = tk.StringVar()


# Widgets
label = ttk.Label(master=window,
                  text="label",
                  textvariable=string_var)
label.pack()

entry = ttk.Entry(master=window,
                  textvariable=string_var)
entry.pack()

window.mainloop()