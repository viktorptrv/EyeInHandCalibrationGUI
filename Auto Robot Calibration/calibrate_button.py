import customtkinter as ctk


class CalibrateButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Calibrate')
        self.configure(text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)


class NullButton(ctk.CTkButton):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(fg_color='black')
        self.configure(state='disabled')
