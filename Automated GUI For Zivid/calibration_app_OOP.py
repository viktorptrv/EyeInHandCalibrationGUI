import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from CTkToolTip import *
from fanucpy import Robot
# from warmup import warmup
# from get_camera_intrinsics import _main
# from hand_in_eye_calibration import calibrate_hand_eye
# from manual_hand_eye_calibration import manual_calibrate_hand_eye


def get_curposv2(self, uframe, tframe) -> list[float]:
    """Gets current cartesian position of tool center point.

    Returns:
        list[float]: Current positions XYZWPR.
    """

    cmd = f"curpos:{uframe}:{tframe}"
    print(cmd)
    _, msg = self.send_cmd(cmd)
    print(f"msg : {msg}")
    vals = [float(val.split("=")[1]) for val in msg.split(",")]
    print(f"Vals : {vals}")
    return vals


def connect_to_cam():
    pass


def connect_to_robot():
    global robot_fanuc

    # Initializing the robot
    robot_fanuc = Robot(
        robot_model="LHMROB011",
        host="10.37.115.206",
        port=18735,
        ee_DO_type="RDO",
        ee_DO_num=7,
    )

    return robot_fanuc


def warmup():
    pass


def get_intr_param():
    pass


def convert_to_halcon():
    pass


def auto_calibration():
    pass


def manual_calibration():
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Calibration App')
        self.geometry('1200x800')

        # Add widgets
        self.TopMenu = TopMenu(self)
        self.MiddleMenuTop = MiddleMenuTop(self)
        self.MiddleMenuMid = MiddleMenuMid(self)
        self.MiddleMenuBottom = MiddleMenuBottom(self)
        self.RightMenuTop = RightMenuTop(self)
        self.RightMenuMid = RightMenuMid(self)
        # self.DropDownMenu = DropDownMenu(self)

        self.iconbitmap('calibration-icon-24.ico')
        # Run the window
        self.mainloop()


class TopMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.button_rob = None
        self.button_cam = None
        self.button_calibration_auto = None
        self.button_calibration_manual = None

        self.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.9)

        self.create_widgets()

    def create_widgets(self):
        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=connect_to_robot)
        self.button_rob.pack(pady=10, padx=10, side='top')

        self.button_cam = ctk.CTkButton(master=self,
                                        text='Connect to Camera',
                                        command=connect_to_cam)
        self.button_cam.pack(pady=10, padx=10, side='top')

        self.button_calibration_auto = ctk.CTkButton(master=self,
                                                     text='Auto Calibration',
                                                     command=auto_calibration)
        self.button_calibration_auto.pack(pady=10, padx=10, side='top')
        CTkToolTip(self.button_calibration_auto, message='For automated calibration you need\n'
                                                         'at least 20 predefined positions of the robot\n'
                                                         'and you must input them in the menu')

        self.button_calibration_manual = ctk.CTkButton(master=self,
                                                       text='Manual Calibration',
                                                       command=manual_calibration)
        self.button_calibration_manual.pack(pady=10, padx=10, side='top')
        CTkToolTip(self.button_calibration_manual, message='For manual calibration you need\n'
                                                           'at least 20 positions of the robot.\n'
                                                           'Change the position of the robot and press'
                                                           'Get Current Position')


class RightMenuTop(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.585, rely=0.02, relwidth=0.4, relheight=0.45)


class RightMenuMid(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.585, rely=0.473, relwidth=0.4, relheight=0.45)


# Used for calibration output
class MiddleMenuBottom(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.23, rely=0.65, relwidth=0.35, relheight=0.272)


class MiddleMenuTop(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.23, rely=0.02, relwidth=0.35, relheight=0.3)


class MiddleMenuMid(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.23, rely=0.325, relwidth=0.35, relheight=0.3)




robot_fanuc = None

ctk.set_appearance_mode('')
ctk.set_default_color_theme('green')
# Running the app
App()
