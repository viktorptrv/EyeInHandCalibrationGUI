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

        self.pack(padx=10, pady=10, fill='both', expand=True)

        self.connected_robot = False
        self.connected_camera = False
        self.connect_cam_button = None
        self.button_rob = None
        self.camera = None
        self.label = None
        self.frame_buttons = None
        self.button_show_pic = None
        self.button_show_depth = None
        self.entry_pose = None
        self.combobox = None
        self.values = ['Choose an Option', 'Get Current Pose', 'Get Current JPose']
        self.box_variable = tk.StringVar(value=self.values[0])

        self.robot_fanuc = Robot(
            robot_model="LHMROB011",
            host="10.37.115.206",
            port=18735,
            ee_DO_type="RDO",
            ee_DO_num=7)

        self.list = []
        self.pose_entry = None
        self.manual_calib = None
        self.automated_calib = None

        self.image = Image.open("dark_python.png")
        self.background_image = ImageTk.PhotoImage(self.image)

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
        self.rowconfigure(index=6, weight=1)
        self.rowconfigure(index=7, weight=1)
        self.rowconfigure(index=8, weight=1)
        self.rowconfigure(index=9, weight=1)
        self.rowconfigure(index=10, weight=1)
        self.rowconfigure(index=11, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.connect_cam_button = ctk.CTkButton(master=self,
                                                text='Connect to Camera',
                                                command=self.connect_to_cam)
        self.connect_cam_button.grid(row=0, column=0, columnspan=2)

        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=self.init_robot)
        self.button_rob.grid(row=0, column=3, columnspan=2)

        self.combobox = ctk.CTkComboBox(master=self,
                                        values=self.values,
                                        variable=self.box_variable,
                                        state='readonly')
        self.combobox.grid(row=0, column=5, padx=10, pady=10)

        self.automated_calib = ctk.CTkButton(master=self,
                                             text='Auto Calibration',
                                             command=self.auto_calibration)
        self.automated_calib.grid(row=1, column=1, columnspan=3)

        CTkToolTip(self.automated_calib, message='For automated calibration you need\n'
                                                 'at least 20 predefined positions of the robot\n'
                                                 'and you must input them in the menu')

        self.manual_calib = ctk.CTkButton(master=self,
                                          text='Manual Calibration',
                                          command=self.manual_calibration)
        self.manual_calib.grid(row=1, column=3, columnspan=3)
        CTkToolTip(self.manual_calib, message='For manual calibration you need\n'
                                              'at least 20 positions of the robot.\n'
                                              'Change the position of the robot and press'
                                              'Get Current Position')

        self.entry_pose = ctk.CTkEntry(master=self)
        self.entry_pose.grid(row=2, column=0, columnspan=6, rowspan=3, sticky='nswe')

        self.button_show_pic = ctk.CTkButton(master=self,
                                             text='Show Picture',
                                             command=self.show_pic)
        self.button_show_pic.grid(row=5, column=1, columnspan=3)

        self.button_show_depth = ctk.CTkButton(master=self,
                                               text='Show Depth map',
                                               command=self.show_depth)
        self.button_show_depth.grid(row=5, column=3, columnspan=3)

        self.background_image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self, image=self.background_image)
        self.label.grid(row=6, column=0, columnspan=6, rowspan=5, sticky='nswe')

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

    def auto_calibration(self):
        # calibrate_hand_eye(robot_joints=)
        pass

    def manual_calibration(self):
        # manual_calibrate_hand_eye(robot=self.robot_fanuc)
        pass

    def show_depth(self):
        pass

    def show_pic(self):
        pass

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.image.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.background_image)

    def get_curr_pose(self):
        global cur_pose

        self.robot_fanuc.get_curpos = get_curposv2
        cur_pose = self.robot_fanuc.get_curpos(self.robot_fanuc, 8, 8)

        return cur_pose


cur_pose = None
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

App()