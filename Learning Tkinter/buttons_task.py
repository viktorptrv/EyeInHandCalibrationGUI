import tkinter as tk
from tkinter import ttk


def print_radio_values():
    print(value_var.get())


def print_check_button_value():
    print(check_button_value_var.get())
    check_button_value_var.set(0)


window = tk.Tk()
window.geometry('400x800')
window.title('Task')

value_var = tk.StringVar()
check_button_value_var = tk.IntVar()

check_button = ttk.Checkbutton(master=window,
                               text='Check button',
                               offvalue=0,
                               onvalue=1,
                               variable=check_button_value_var,
                               command=print_radio_values)
check_button.pack()


radio_button_one = ttk.Radiobutton(master=window,
                                   text='Radio one',
                                   value='A',
                                   variable=value_var,
                                   command=print_check_button_value)
radio_button_one.pack()
radio_button_two = ttk.Radiobutton(master=window,
                                   text='Radio two',
                                   value='B',
                                   variable=value_var,
                                   command=print_check_button_value)
radio_button_two.pack()
window.mainloop()