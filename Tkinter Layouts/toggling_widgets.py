"""
In tkinter you don't really hide/reveal widgets.
Instead you remove and add widgets to the layout.
Pack to place a widget
pack_forget to remove it
The forget method works only once
To have proper toggle functionality create another variable
"""

import tkinter as tk
from tkinter import ttk


# def toggle_label_place():
#     global label_vis
#
#     if label_vis:
#         label.place_forget()
#         label_vis = False
#     else:
#         label.place(relx=0.5, rely=0.5, anchor='center')
#         label_vis = True


def toggle_label_grid():
    global label_vis

    if label_vis:
        label_vis = False
        label.grid_remove()
    else:
        label_vis = True
        label.grid(row=0, column=1)


window = tk.Tk()
window.geometry('600x400')

# # Place
# button = ttk.Button(master=window,
#                     text='Toggle label',
#                     command=toggle_label_place)
# button.place(x=10, y=50)
#
# # Creating a variable for toggle functionality
# label_vis = True
# label = ttk.Label(master=window,
#                   text='Label')
# label.place(relx=0.5, rely=0.5, anchor='center')


# Grid
window.columnconfigure(0, weight=1, uniform='a')
window.rowconfigure(0, weight=1, uniform='a')

button = ttk.Button(master=window,
                    text='Toggle label',
                    command=toggle_label_grid)
button.grid(row=0, column=0)

# Creating a variable for toggle functionality
label_vis = True
label = ttk.Label(master=window,
                  text='Label')
label.grid(row=0, column=1)

window.mainloop()
