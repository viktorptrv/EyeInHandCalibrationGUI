import tkinter as tk

import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from robot_button import RobotButton
from Menu_One import FrameLeft
from Menu_Two import FrameRight
from camera_button import CameraButton


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

        self.MenuLeft = FrameLeft(self)
        self.MenuLeft.grid(column=0, row=0, columnspan=3, rowspan=6, sticky='nswe')

        self.MenuRight = FrameRight(self)
        self.MenuRight.grid(column=3, row=0, columnspan=3, rowspan=6, sticky='nswe')

        self.RobotButton = RobotButton(self.MenuLeft)
        self.RobotButton.grid(row=0, column=1, padx=10, pady=10)

        self.CameraButton = CameraButton(self.MenuLeft)
        self.CameraButton.grid(row=0, column=3, padx=10, pady=10)

        # self.MenuLeft = None
        # self.MenuRight = None
        # self.RobotButton = None
        # self.CameraButton = None

        # self.create_widgets()

    # def create_widgets(self):
    #     """
    #     Creating and Placing the widgets
    #     """
    #     self.MenuLeft = FrameLeft(self)
    #     self.MenuLeft.grid(column=0, row=0, columnspan=3, rowspan=6, sticky='nswe')
    #
    #     self.MenuRight = FrameRight(self)
    #     self.MenuRight.grid(column=3, row=0, columnspan=3, rowspan=6, sticky='nswe')
    #
    #     self.RobotButton = RobotButton(self.MenuLeft)
    #     self.RobotButton.grid(row=0, column=0)
    #
    #     self.CameraButton = CameraButton(self.MenuLeft)
    #     self.CameraButton.grid(row=0, column=3)


if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    """
    First we create the object and then we run it wil mainloop.
    This way it will create all the needed widgets and run all the threads
    """

    app = App()
    app.mainloop()
