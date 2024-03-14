"""
Pack is easier to use when combined with frames
Layouts are created in a single direction
Some items are frames that contain their own layout
"""

import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x600')
window.title('Packs')

top_frame = ttk.Frame(master=window)

label1 = ttk.Label(master=top_frame, text='First label', background='red')

label2 = ttk.Label(master=top_frame, text='Second label', background='blue')

label3 = ttk.Label(master=window, text='Third label', background='green')

label4 = ttk.Label(master=window, text='Fourth label', background='orange')

button = ttk.Button(master=window,
                    text='A button')

button2 = ttk.Button(master=window,
                     text='A second button')
# top layout

# top_frame.pack()
# label1.pack()
# label2.pack()
# button.pack()
# button.pack(side='bottom')


"""
Expand method - determines how much space a widget CAN occupy
The widget expands only in 1 direction
width is not set by expand if side is top or bottom
height is set by expand but only vertically
Widget is only big as the text it needs to display
however the widget can occupy more space by default
If side is top or bottom, widgets can occupy the entire width of the container
Expand tells the widget that it can take up all of the available space in one direction
side = top/bottom => widget can be as wide as the container, expand determines the height
side = left/right => widget can be as height as the container, expand determines the width
"""

# top_frame.pack()
# label1.pack(side='top', expand=True)
# label2.pack(side='top', expand=True)
# label3.pack(side='top', expand=True)
# button.pack(side='top', expand=True)

"""
The fill method- x, y, both, none
Determines if a widget will occupy the the available space
both - entire space
"""
# top_frame.pack()
# label1.pack(side='top', fill='both')
# label2.pack(side='top', expand=True)
# label3.pack(side='top', expand=True, fill='both')
# button.pack(side='top', fill='x')

"""
padding - padx/pady
Creates space around the widget
and fills it with white space
ipadx/ipady - creates padding inside the widget which expands the widget

"""

top_frame.pack()
label1.pack(side='top', fill='both', pady=50)
label2.pack(side='top', expand=True, ipady=50, ipadx=50)
label3.pack(side='top', expand=True, fill='both')
button.pack(side='top', fill='x')


window.mainloop()
