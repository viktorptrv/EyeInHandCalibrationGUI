import customtkinter as ctk
from CTkToolTip import *
import tkinter


class AutoCalibrate(ctk.CTkCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.check_var_auto = ctk.IntVar()
        self.configure(text="Automatic Calibration")
        self.configure(variable=self.check_var_auto)
        CTkToolTip(self, message='For automated calibration you need\n'
                                  'at least 20 predefined positions of the robot\n'
                                  'and you must input them in the entry bellow')


class ManualCalibrate(ctk.CTkCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.check_var_manual = ctk.IntVar()
        self.configure(text="Manual Calibration")
        self.configure(variable=self.check_var_manual)

        CTkToolTip(self, message='For manual calibration you need\n'
                                 'at least 20 positions of the robot.\n'
                                 'Change the position of the robot and press '
                                 'Get Current Position')
