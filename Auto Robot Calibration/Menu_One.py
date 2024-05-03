import tkinter as tk
import customtkinter as ctk
# from main import App


class FrameLeft(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color='green')
        self.grid(column=0, row=0, columnspan=3, rowspan=6,  sticky='nswe')


# App.MenuLeft = FrameLeft(App)