import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk
from Menu_One import FrameLeft


class RobotButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Hello')
        self.configure(fg_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)

        # self.grid(row=0, column=3, padx=10, pady=10)




# FrameLeft.robot = RobotButton(FrameLeft)