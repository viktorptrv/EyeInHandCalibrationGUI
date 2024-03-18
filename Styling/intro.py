"""
- Inbuilt styling tools - terrible
- External themes - terrible
- External modules (customtkinter and ttkbootstrap)
"""

import tkinter as tk
from tkinter import ttk, font

window = tk.Tk()
window.geometry('600x600')
window.title('Styling')

# Creating a style object
style = ttk.Style()
style.theme_use('classic')  # Using a style configure

# First we input the name of the widget which we want to configure
# But we have to always add T before the name
style.configure(style='new.TButton',
                foreground='green',
                font=('Roman', 20))
style.map('new.TButton',
          foreground=[('pressed', 'red'), ('disabled', 'yellow')],
          background=[('pressed', 'green'), ('active', 'blue')])

# Print all font styles
print(font.families())

label = ttk.Label(master=window,
                  text='Roman',
                  background='red',
                  foreground='white',
                  font=('', 22))
label.pack()

# We can't really style a button, because ttk
# Widgets are more modern
button = ttk.Button(master=window,
                    text='A button',
                    style='new.TButton')
button.pack()

window.mainloop()