import customtkinter as ctk


class TextPoses(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(scrollbar_button_color='#2DFE54')
