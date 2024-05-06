import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk
from Menu_One import FrameLeft


class RobotButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Connect Robot')
        self.configure(fg_color='#ffba33')
        self.configure(text_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)

