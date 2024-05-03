import tkinter as tk

import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
# from robot_button import RobotButton


class App(ctk.CTk):
    def __init__(self):
        super().__init__() # With the super method we give a master

        self.title('Calibration App')
        self.geometry('1100x500')
        self.maxsize(1100, 500)
        self.minsize(1100, 500)

        self.columnconfigure(index=(0,1,2,3,4,5), weight=1)

        self.RobButton = RobotButton(self)  # Adding a button

        self.mainloop()


if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    App()