import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from CTkToolTip import *


class LoadFileButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Load File with Poses')
        self.configure(fg_color='#2DFE54')
        self.configure(text_color='black')
    #     self.configure(command=self.load_file)
    #     self.file_types = (('text files', '*.txt'),
    #                        ('All files', '*.*'))
    #
    #     self.text = tk.Text(parent, height=12)
    #
    # def load_file(self):
    #     file = fd.askopenfile(filetypes=self.file_types,
    #                           initialdir="D:/Downloads")
    #
    #     self.text.insert('1.0', file.readlines())
