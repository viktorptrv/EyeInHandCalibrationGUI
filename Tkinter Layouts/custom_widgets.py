"""
We can create custom widgets
Classes - you inherit from a widget and add custom parts. Suitable for creating complex layouts
But you can create lots of classes
Functional - you create a widget in a function and return it. This will be more limited for the layouts.
But it's easier to organise
"""
import tkinter as tk
from tkinter import ttk


class Segment(ttk.Frame):
    def __init__(self, parent, label_text, button_text):
        super().__init__(master=parent)
        # Grid layout
        self.rowconfigure(index=0, weight=1)
        self.columnconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=1, weight=1, uniform='a')
        self.columnconfigure(index=2, weight=1, uniform='a')
        ttk.Label(self, text=label_text).grid(row=0, column=0, sticky='nswe')
        ttk.Button(self, text=button_text).grid(row=0, column=1, sticky='nswe')
        self.pack(expand=True, fill='both')


window = tk.Tk()
window.title('widgets and returns')
window.geometry('400x600')

# Widgets are to be created in the global scope
Segment(window, 'label', 'button')
Segment(window, 'test', 'click')
Segment(window, 'hello', 'test')
Segment(window, 'kur', 'test')
Segment(window, 'kor', 'test')


window.mainloop()