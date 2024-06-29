import tkinter as tk
import customtkinter as ctk

from CTkToolTip import *
from PIL import Image, ImageTk
from Menu_One import FrameLeft


class IntrButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Intrinsics')
        self.configure(fg_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)
        CTkToolTip(self, message='The intrinsic parameters represent the optical center '
                                 'and focal length of the camera.')



