"""
When using the grid method for placement of a widget
you can set the number of rows and columns,
you can set the width/height of each column/row
Grid determines how much space a widget can occupy
Sticky determines what will be filled - North, East, West, South
stick='n' -> widget retains size but sticks at the top
stick='ns' -> widget retains width but height is height of the cell
Grid always scales with the window
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('600x400')
window.title('Grid')

label1 = ttk.Label(master=window, text='Label1', background='red')
label2 = ttk.Label(master=window, text='Label2', background='blue')
label3 = ttk.Label(master=window, text='Label3', background='green')
label4 = ttk.Label(master=window, text='Label4', background='yellow')
button1 = ttk.Button(master=window, text='A button')
button2 = ttk.Button(master=window, text='another button')
entry = ttk.Entry(master=window)

# Define a grid
# columnconfigure creates one or multiple columns
# index = number of columns
# weight = what is the width of the column
window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.columnconfigure(index=3, weight=1)

# Creating a row
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)

# Place a widget
# Placing the widget leaves a ton of white space
# to get rid of the white space use the sticky argument
# label1.grid(row=0, column=0, sticky='nswe')
label2.grid(row=1, column=1, sticky='nswe')
label3.grid(row=2, column=3, sticky='nswe')
label4.grid(row=2, column=2, sticky='nswe')

# rowspan tells the widget how many rows it should occupy
# by default its 1
label1.grid(row=0, column=0, rowspan=2, sticky='nswe')
label2.grid(row=0, column=0, columnspan=2, sticky='nswe')


window.mainloop()