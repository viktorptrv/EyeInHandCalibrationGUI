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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Calibration App')
        self.geometry('600x800')

        # Add widgets
        self.TopMenu = TopMenu(self)
        self.DropDownMenu = DropDownMenu(self)

        # Run the window
        self.mainloop()


class TopMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.button_rob = None
        self.button_cam = None

        self.place(relx=0.2, rely=0.05, relwidth=0.55, relheight=0.08)

        self.create_widgets()

    def create_widgets(self):
        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=connect_to_robot)
        self.button_rob.pack(pady=10, padx=10, side='left')

        self.button_cam = ctk.CTkButton(master=self,
                                        text='Connect to Camera',
                                        command=connect_to_cam)
        self.button_cam.pack(pady=10, padx=10, side='right')


class DropDownMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.warmup_button = None
        self.intrinsics_button = None
        self.convert_to_halcon_intr = None

        self.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.08)

        self.create_widgets()

    def create_widgets(self):
        self.warmup_button = ctk.CTkButton(master=self,
                                           text='Warm up',
                                           command=warmup)
        self.warmup_button.pack(pady=10, padx=10, side='left')

        CTkToolTip(self.warmup_button, message='To warm up the camera is essential\n'
                                               'if the camera has not been used in a while')

        self.intrinsics_button = ctk.CTkButton(master=self,
                                               text="Intrinsics Parameters",
                                               command=get_intr_param)
        self.intrinsics_button.pack(pady=10, padx=10, side='left')

        CTkToolTip(self.intrinsics_button, message='Get intrinsics parameters\nof the zivid camera')

        self.convert_to_halcon_intr = ctk.CTkButton(master=self,
                                                    text='Convert to Halcon',
                                                    command=convert_to_halcon)
        self.convert_to_halcon_intr.pack(pady=10, padx=10, side='left')

        CTkToolTip(self.convert_to_halcon_intr, message='Convert Zivid Intrinsics parameters\n'
                                                        'to be suitable for Halcon - check documentation')


robot_fanuc = None

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')
# Running the app
App()
