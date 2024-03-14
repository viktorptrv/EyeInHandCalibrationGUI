"""
Widgets are place by specifying the left,top, width and height
These numbers can be absolute or relative
Absolute - from the x and y direction, width and height
Relative - separating the whole window as a coordinate system,
in which the top left is (0,0) - (relx=0.1, rely=0.2)
Relative values scale along the window
"""

import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x600')

label1 = ttk.Label(master=window, text='Label1', background='red')
label2 = ttk.Label(master=window, text='Label2', background='blue')
label3 = ttk.Label(master=window, text='Label3', background='green')
button1 = ttk.Button(master=window, text='A button')

# layout
label1.place(x=5, y=50, width=50, height=20)

# The anchor controls which point is placed
# By default is the top left point
button1.place(relx=0.6, rely=0.1, anchor='se')

window.mainloop()
