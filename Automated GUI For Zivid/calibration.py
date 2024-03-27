import tkinter as tk

import customtkinter
import customtkinter as ctk
# import zivid
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *
from fanucpy import Robot
from PIL import Image, ImageTk
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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Calibration App')
        self.geometry('500x800')
        self.maxsize(500, 800)
        self.minsize(500, 800)
        self.iconbitmap('calibration-icon-24.ico')

        self.Menu = Menu(self)

        self.mainloop()


class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(padx=10, pady=10)

        self.connected_robot = False
        self.connected_camera = False
        self.connect_cam_button = None
        self.button_rob = None
        self.camera = None

        self.combobox = None
        self.values = ['Choose an Option', 'Get Current Pose', 'Get Current JPose']
        self.box_variable = tk.StringVar(value=self.values[0])

        self.robot_fanuc = Robot(
            robot_model="LHMROB011",
            host="10.37.115.206",
            port=18735,
            ee_DO_type="RDO",
            ee_DO_num=7)

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)
        self.columnconfigure(index=4, weight=1)
        self.columnconfigure(index=5, weight=1)

        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.rowconfigure(index=4, weight=1)
        self.rowconfigure(index=5, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.connect_cam_button = ctk.CTkButton(master=self,
                                                text='Connect to Camera',
                                                command=self.connect_to_cam)
        self.connect_cam_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=self.init_robot)
        self.button_rob.grid(row=0, column=3, columnspan=2, padx=10, pady=10)

        self.combobox = ctk.CTkComboBox(master=self,
                                        values=self.values,
                                        variable=self.box_variable,
                                        state='readonly')
        self.combobox.grid(row=0, column=5, padx=10, pady=10)

    def connect_to_cam(self):
        if not self.connected_camera:
            try:
                app = zivid.Application()
                self.camera = app.connect_camera()
                self.connected_camera = True
            except Exception:
                messagebox.showinfo('Error', 'You could not connect to the camera!\n'
                                                 'Check your network!')
                self.connected_camera = False

            else:
                messagebox.showinfo('Connected!', 'Camera is connected!')

    def init_robot(self):
        try:
            self.robot_fanuc.connect()
            self.connected_robot = True

        except Exception:
            messagebox.showinfo('Error!', 'You could not connect to the robot!\n'
                                          'Check your network!')
            self.connected_robot = False

        finally:
            if not self.connected_robot:
                self.combobox.configure(state='readonly')
                CTkToolTip(self.combobox, message='Since you are not connected to the robot\n'
                                                  'the options are only readable')

            else:
                self.combobox.configure(state='normal')
                self.combobox.bind('<<ComboboxSelected>>', self.selected_option)

    def selected_option(self, event):
        pass
    #     # if == 'Get Curr Pose':
    #     #     print('cur pose')
    #     # else:
    #     #     print('kor')

    def get_curr_pose(self):
        global cur_pose

        self.robot_fanuc.get_curpos = get_curposv2
        cur_pose = self.robot_fanuc.get_curpos(self.robot_fanuc, 8, 8)

        return cur_pose

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

App()