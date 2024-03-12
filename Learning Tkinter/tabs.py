"""
When needed to create tabs we are using ttk.Notebook
Has a couple of children (which are frames)
Each frame is one tab
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x700')
window.title('Tabs')

# Creating a notebook widget
notebook = ttk.Notebook(master=window)
notebook.pack()

# Creating a tab
tab1 = ttk.Frame(master=notebook)
tab2 = ttk.Frame(master=notebook)

# To see the tabs
notebook.add(tab1, text='Tab 1')
notebook.add(tab2, text='Tab 2')

label = ttk.Label(master=tab1,
                  text='text in tab 1')
label.pack()

button = ttk.Radiobutton(master=tab2,
                         text='Button in tab 2',
                         command=lambda: print('ok'))
button.pack()

window.mainloop()