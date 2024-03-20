import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from CTkToolTip import *
from fanucpy import Robot


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


ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

window = ctk.CTk()
window.geometry('600x800')
window.title('Calibration')


# Top frame layout
top_frame = ctk.CTkFrame(master=window)
top_frame.place(relx=0.2, rely=0.05, relwidth=0.55, relheight=0.08)

button_rob = ctk.CTkButton(master=top_frame,
                           text='Connect to Robot',
                           command=connect_to_robot)
button_rob.pack(pady=10, padx=10, side='left')

button_cam = ctk.CTkButton(master=top_frame,
                           text='Connect to Camera',
                           command=connect_to_cam)
button_cam.pack(pady=10, padx=10, side='right')


# Drop down frame
drop_frame = ctk.CTkFrame(master=window)
drop_frame.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.08)

warmup_button = ctk.CTkButton(master=drop_frame,
                              text='Warm up',
                              command=warmup)
warmup_button.pack(pady=10, padx=10, side='left')

CTkToolTip(warmup_button, message='To warm up the camera is essential\n'
                                  'if the camera has not been used in a while')

intrinsics_button = ctk.CTkButton(master=drop_frame,
                                  text="Intrinsics Parameters",
                                  command=get_intr_param)
intrinsics_button.pack(pady=10, padx=10, side='left')

CTkToolTip(intrinsics_button, message='Get intrinsics parameters\nof the zivid camera')

convert_to_halcon_intr = ctk.CTkButton(master=drop_frame,
                                       text='Convert to Halcon',
                                       command=convert_to_halcon)
convert_to_halcon_intr.pack(pady=10, padx=10, side='left')

CTkToolTip(convert_to_halcon_intr, message='Convert Zivid Intrinsics parameters\n'
                                           'to be suitable for Halcon - check documentation')


window.mainloop()