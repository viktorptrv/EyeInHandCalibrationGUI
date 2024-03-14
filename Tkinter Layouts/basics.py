import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('400x600')

label1 = ttk.Label(master=window, text='Label1', background='red')
label2 = ttk.Label(master=window, text='Label2', background='blue')
label3 = ttk.Label(master=window, text='Label3', background='green')
label4 = ttk.Label(master=window, text='Label4', background='yellow')
button1 = ttk.Button(master=window, text='A button')
button2 = ttk.Button(master=window, text='another button')
entry = ttk.Entry(master=window)
window.mainloop()