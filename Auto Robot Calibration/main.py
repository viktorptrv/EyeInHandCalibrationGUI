import tkinter as tk

import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from robot_button import RobotButton
from Menu_One import FrameLeft


class App(ctk.CTk):
    def __init__(self):
        super().__init__() # With the super method we include a master

        self.title('Calibration App')
        self.geometry('1100x500')
        self.maxsize(1100, 500)
        self.minsize(1100, 500)

        self.robot_button = None
        self.camera_button = None

        # Configuring the grid of the window
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)
        self.columnconfigure(index=4, weight=1)
        self.columnconfigure(index=5, weight=1)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.rowconfigure(index=4, weight=1)
        self.rowconfigure(index=5, weight=1)

        self.MenuLeft = None
        self.robot = None

        self.create_widgets()

    def create_widgets(self):
        self.MenuLeft = FrameLeft(self)
        self.robot = RobotButton(self)
        self.MenuLeft.grid(column=0, row=0, columnspan=3, rowspan=6,  sticky='nswe')
        self.robot.grid(row=0, column=3, padx=10, pady=10)




if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    app = App()
    app.mainloop()
