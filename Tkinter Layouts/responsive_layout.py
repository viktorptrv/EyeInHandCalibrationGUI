"""
Tkinter lacks inbuilt tools for responsive layouts. We cannot update an existing layout
We need to create a separate layout for each window size.
We are setting break points for the minimum width of a layout
From a width of 300 - small layout - 299 to 300
From a width of 600 - medium layout
From a width of 1200 - large layout
Whenever the window resizes we check the width and if it crosses a threshold we build a new layout
"""
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self, start_size):
        super().__init__()
        self.title('Responsive layout')
        self.geometry(f'{start_size[0]}x{start_size[1]}')

        # Event that gets the configuration of the window
        self.bind('<Configure>', lambda event: print(event))
        self.mainloop()


app = App((400, 300))