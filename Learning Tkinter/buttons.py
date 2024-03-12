import tkinter as tk
from tkinter import ttk


def button_func_1():
    print('a basic button')
    # getting the variable value from the radio buttons
    print(radio_var.get())


window = tk.Tk()
window.geometry('250x700')
window.title("Buttons")

button_string = tk.StringVar(value="button")
button = ttk.Button(master=window,
                    text='simple button',
                    command=button_func_1,
                    textvariable=button_string)
button.pack()

check_button = ttk.Checkbutton(master=window,
                               text='check button',
                               command=lambda: print('check'))
check_button.pack()

# With radio buttons always change the default value
radio_var = tk.StringVar()
radio_button_one = ttk.Radiobutton(master=window,
                                   text="Radio Button one",
                                   value=1,
                                   variable=radio_var)
radio_button_one.pack()

radio_button_two = ttk.Radiobutton(master=window,
                                   text='Radio Button Two',
                                   value=2,
                                   variable=radio_var)

radio_button_two.pack()




window.mainloop()