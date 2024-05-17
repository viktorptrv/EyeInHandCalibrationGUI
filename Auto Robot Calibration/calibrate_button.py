import customtkinter as ctk
from CTkToolTip import *


class CalibrateButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(state='disable')
        self.configure(text='Calibrate')
        self.configure(text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)
        CTkToolTip(self, message='For automated calibration you need\n'
                                  'at least 20 predefined positions of the robot\n'
                                  'and you must input them in the menu\n')



# class NullButton(ctk.CTkButton):
#     def __init__(self,parent):
#         super().__init__(parent)
#         self.configure(fg_color='black')
#         self.configure(state='disabled')

