"""
Pack used with frames create a better layouts
Layouts are created only in one direction
Some frames can contain their own layouts
"""
import tkinter as tk
from tkinter import ttk

import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x600')
window.title('Packs')

# Frame 1
top_frame = ttk.Frame(master=window)

label1 = ttk.Label(master=top_frame, text='First label', background='red')

label2 = ttk.Label(master=top_frame, text='Second label', background='blue')

# Middle widget
label3 = ttk.Label(master=window, text='Third label', background='green')

# Bottom frame
bottom_frame = ttk.Frame(master=window)
label4 = ttk.Label(master=bottom_frame, text='Fourth label', background='orange')

button = ttk.Button(master=bottom_frame, text='A button')

button2 = ttk.Button(master=bottom_frame,
                     text='A second button')

# Top layout
top_frame.pack(fill='both', expand=True)
label1.pack(fill='both', expand=True)
label2.pack(fill='both', expand=True)

# Middle layout
label3.pack(expand=True)

# Bottom layout
bottom_frame.pack(expand=True, padx=20, pady=20, fill='both')
button.pack(side='left', expand=True, fill='both')
label4.pack(side='left', expand=True, fill='both')
button2.pack(side='left', expand=True, fill='both')

window.mainloop()