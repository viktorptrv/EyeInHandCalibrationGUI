import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('500x800')

items = ('Ice', 'Water', 'Broccoli')
# on startup the selected item will be the first element from the tuple
food_string = tk.StringVar(value=items[0])
menu = ttk.Combobox(master=window,
                    textvariable=food_string)
# Assigning values to the combobox:
menu['values']=items
menu.config(values=items)
menu.pack()

# events every time an option from the menu is selected, the event
# will trigger and it will execute the function
menu.bind('<<ComboboxSelected>>', lambda event: print(food_string.get()))

# Spinbox
spin = ttk.Spinbox(window,
                   from_=3,
                   to=20,
                   increment=2,
                   command=lambda : print('Pressed'))
spin.bind('<<Increment>>', lambda event: print('up'))
spin.bind('<<Decrement>>', lambda event: print('Down'))
# spin['value']=(1, 2, 3, 4, 5)
spin.pack()

window.mainloop()
