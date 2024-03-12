"""
In tkinter menu is created with tk.Menu
To create more complex menus
You must use several menus and nest them
If you place a tk.menu inside of another
tk.Menu it becomes one option
For a sub menu you would place a menu inside of a menu
inside of a menu
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('600x400')
window.title('Menu')

# Creating a menu
menu = tk.Menu(master=window)
# Packing the menu
window.config(menu=menu)

# Sub menu
file_menu = tk.Menu(master=menu,
                    tearoff=False) # tearoff removes '----'

# Adding the sub menu to the main menu
menu.add_cascade(label='File', menu=file_menu)

file_menu.add_command(label='New',
                      command=lambda: print('New file'))
file_menu.add_command(label='File',
                      command=lambda: print('Open File'))
file_menu.add_separator()


# Another sub menu
help_menu = tk.Menu(master=menu,
                    tearoff=False)

# Adding the sub menu to the main menu
menu.add_cascade(label='Help Menu', menu=help_menu)
help_menu.add_command(label='Help Entry',
                      command=lambda: print('Help entry'))
help_check_str_value = tk.StringVar()
help_menu.add_checkbutton(label='check',
                          offvalue='Off',
                          onvalue='On',
                          variable=help_check_str_value)

# Menu button
menu_button = ttk.Menubutton(master=window,
                             text='Menu button')
menu_button.pack()

# Adding tk.Menu to menu_button
sub_menu_button = tk.Menu(master=menu_button,
                          tearoff=False)
sub_menu_button.add_command(label='Entry',
                            command=lambda: print('Test one'))
# Add sub menu to main menu
menu_button.config(menu=sub_menu_button)

window.mainloop()