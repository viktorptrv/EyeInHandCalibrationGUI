# Events can be:
# - Keyboard inputs
# - Widgets getting changed
# - Widgets gets selected/unselected
# - Mouse clock/motion/wheel
# Events can be observed and used - run a function on a button press
# Events need to be bind to a widget
# Widget.bind(event, function)

import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x800')

text = tk.Text(master=window)
text.pack()

entry = ttk.Entry(master=window)
entry.pack(pady=10)

btn = ttk.Button(master=window,
                 text="A button")
btn.pack()

# Events <modifier-type-detail>
window.bind('<Alt-KeyPress-a>', lambda event: print('event'))

# Event working only with the button
btn.bind('<Alt-KeyPress-a>', lambda event: print('event'))

window.mainloop()