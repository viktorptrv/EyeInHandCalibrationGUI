import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk


class CameraButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Connect Camera')
        self.configure(fg_color='#ffba33')
        self.configure(text_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)
        self.configure(command=self.remove_image)

    def remove_image(self):
        from main import WarmUpBlur

        WarmUpBlur.place_forget(self)

