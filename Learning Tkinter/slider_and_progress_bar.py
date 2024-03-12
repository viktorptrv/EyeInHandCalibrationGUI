"""
Sliders and progress bars both show progress in one dimension
The slider can be moved by the user or set independently
The progress bar can only be set independently
"""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

window = tk.Tk()
window.title('Sliders')

# Creating the slider
# Every time when clicking on the scale we are activating the command
scale_int = tk.IntVar(value=10)
scale = ttk.Scale(master=window,
                  command=lambda value: print(scale_int.get()),
                  from_=0,
                  to=25,
                  length=300,
                  orient='vertical',
                  variable=scale_int)
scale.pack()

# progress bar
# progress bar is set by a variable
progress = ttk.Progressbar(master=window,
                           variable=scale_int,
                           maximum=25,
                           orient='horizontal',   #automatically is horizontal
                           mode='indeterminate',
                           length=400)
progress.pack()
# methods for a progress bar
# progress.start()

# scrolledtext IT IS AN IMPORT that contains other widgets
scrolled_text = scrolledtext.ScrolledText(master=window)
scrolled_text.pack()


window.mainloop()