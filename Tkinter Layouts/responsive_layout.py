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

        SizeNotifier(self, {300: self.create_small_layout, 600: self.create_medium_layout})

        # Event that gets the configuration of the window
        # self.bind('<Configure>', lambda event: print(event))
        self.mainloop()

    def create_small_layout(self):
        pass

    def create_medium_layout(self):
        pass


class SizeNotifier:
    def __init__(self, window, size_dict):
        self.window = window
        self.size_dict = {key: value for key, value in sorted(size_dict.items())}
        self.window.bind('<Configure>', lambda event: print(event))

    def check_size(self, event):
        window_width = event.width
        checked_size = None

        for min_size in self.size_dict:
            delta = window_width - min_size


app = App((400, 300))