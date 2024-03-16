"""
We take a tkinter widget(usually a frame) via inheritancce and
add widgets to it. That way we can organize lots of widgets very easily
"""

import tkinter as tk
from tkinter import ttk


class App(tk.Tk):   # The class will inherit from tk.Tk() and the app will be the window
    def __init__(self, title, size):
        super().__init__()
        self.title(title)   # .title is a method of the class .Tk()
        self.geometry(size)

        # Widgets
        self.menu = Menu(self)  # Self is the parent, app itself is the master\
        self.main = Main(self)
        self.mainloop()


class Menu(ttk.Frame):  # Creating a menu and widgets
    def __init__(self, parent):     # parent is self in class App
        super().__init__(parent)    # Super is used to call the object by itself
        self.menu_button1 = None
        self.menu_button2 = None
        self.menu_button3 = None
        self.menu_slider1 = None
        self.menu_slider2 = None
        self.toggle_frame = None
        self.menu_toggle1 = None
        self.menu_toggle2 = None
        self.menu_entry = None

        # Place the frame itself
        self.place(x=0, y=0, relwidth=0.3, relheight=1)

        self.create_widgets() # We have to call the functions
        self.create_layout()

    # Creating widgets in the menu
    def create_widgets(self):
        # Self.variable to make them attributes of the class
        self.menu_button1 = ttk.Button(master=self, text='Button 1')
        self.menu_button2 = ttk.Button(master=self, text='Button 2')
        self.menu_button3 = ttk.Button(master=self, text='Button 3')

        self.menu_slider1 = ttk.Scale(master=self, orient='vertical')
        self.menu_slider2 = ttk.Scale(master=self, orient='vertical')

        self.toggle_frame = ttk.Frame(self)

        button_var = tk.IntVar()

        self.menu_toggle1 = ttk.Checkbutton(master=self.toggle_frame, text='Check 1', onvalue=1, offvalue=0)
        self.menu_toggle2 = ttk.Checkbutton(master=self.toggle_frame, text='Check 2', onvalue=0, offvalue=1)
        self.menu_entry = ttk.Entry(master=self)

    def create_layout(self):
        self.columnconfigure(index=0, weight=1, uniform='a')
        self.columnconfigure(index=1, weight=1, uniform='a')
        self.columnconfigure(index=2, weight=1, uniform='a')

        self.rowconfigure(index=0, weight=1, uniform='a')
        self.rowconfigure(index=1, weight=1, uniform='a')
        self.rowconfigure(index=2, weight=1, uniform='a')
        self.rowconfigure(index=3, weight=1, uniform='a')
        self.rowconfigure(index=4, weight=1, uniform='a')

        self.menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2)
        self.menu_button2.grid(row=0, column=2, sticky='nswe')
        self.menu_button3.grid(row=1, column=0, sticky='nswe', columnspan=3)

        self.menu_slider1.grid(row=2, column=0, sticky='nswe', columnspan=2, pady=20)
        self.menu_slider2.grid(row=2, column=2, sticky='nswe', columnspan=2, pady=20)

        self.toggle_frame.grid(row=4, column=0, columnspan=3, sticky='nswe')

        self.menu_toggle1.pack(side='left', expand=True)
        self.menu_toggle2.pack(side='left', expand=True)

        self.menu_entry.place(relx=0.5, rely=0.95, relwidth=0.9, anchor='center')


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(master=self, text='Test 1', background='red')
        self.button = ttk.Button(self, text='Button')

        self.label.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        self.button.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        self.place(relx=0.3, y=0, relwidth=0.7, relheight=1)


# Creating an instance of the object
App('Class based app', '600x600')