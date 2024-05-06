import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk
from Menu_One import FrameLeft


class WarmUpButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Warm Up')
        self.configure(fg_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)

