"""
Frames are used for better layouts with parenting
A menu item should a menu as the master
A tab entry should have a tab widget as the master
For complex layouts, you can also create a container widget to organise your widgets
A container widget is the frame
ttk.Frame is just an empty widget
You place widgets inside of it and then you place the frame
That way you can arrange widgets easily
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('600x400')

# Creating the frame
# Frames are invisible
# To see the border of the frame use borderwidth and relief
frame = ttk.Frame(master=window,
                  width=100,
                  height=200,
                  borderwidth=20,
                  relief=tk.RIDGE)
frame.pack(side='left')

# master setting (parenting)
# when parenting, the child overrides the width and the height of the parent
# to disable ti use frame.pack_propagate(False) to use the original size
label = ttk.Label(master=frame,
                  text='Frame')
label.pack()
window.mainloop()