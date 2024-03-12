import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('100x100')


values_spin = ['A', 'B', 'C', 'D', 'E']
spin_var = tk.StringVar(value=values_spin[0])
spinbox = ttk.Spinbox(master=window,
                      values=values_spin,
                      textvariable=spin_var)
spinbox.bind('<<Increment>>', lambda event: print(spin_var.get()))
spinbox.pack()


window.mainloop()