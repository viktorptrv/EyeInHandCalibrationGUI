import tkinter as tk
import customtkinter as ctk
import zivid
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *
from fanucpy import Robot
from PIL import Image, ImageTk
from warmup import warmup
from get_camera_intrinsics import camera_intrinsics
from hand_in_eye_calibration import calibrate_hand_eye
from manual_hand_eye_calibration import manual_calibrate_hand_eye


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
        self.geometry('550x800')
        self.maxsize(550, 800)
        self.minsize(550, 800)
        # self.iconbitmap('calibration-icon-24.ico')

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
        self.manual_calib_get_pose_button = None
        self.entry_curr_pose_show = None
        self.camera = None
        self.label = None
        self.frame_buttons = None
        self.button_show_pic = None
        self.button_show_depth = None
        self.entry_pose = None
        self.combobox_rob = None
        self.combobox_cam = None

        self.take_pose_button = None

        self.values = ['Choose an Option', 'Get Current Pose', 'Get Current JPose']
        self.values_cam = ['Choose an Option', 'Warm Up Cam', 'Get Intrinsics']
        self.box_variable = tk.StringVar(value=self.values[0])
        self.box_variable_cam = tk.StringVar(value=self.values_cam[0])
        self.coordinates = {}

        self.manual_calib_on = False
        self.automated_calib_on = False

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

        self.image = Image.open("../../../Desktop/For Mitko/Python/Python Calibration of Zivid/GUI/img.png")
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
        self.rowconfigure(index=12, weight=1)
        self.rowconfigure(index=13, weight=1)
        self.rowconfigure(index=14, weight=1)
        self.rowconfigure(index=15, weight=1)
        self.rowconfigure(index=16, weight=1)
        self.rowconfigure(index=17, weight=1)


        self.create_widgets()

    def create_widgets(self):
        self.connect_cam_button = ctk.CTkButton(master=self,
                                                text='Connect to Camera',
                                                command=self.connect_to_cam)
        self.connect_cam_button.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=self.init_robot)
        self.button_rob.grid(row=0, column=3, columnspan=3, pady=10)

        self.combobox_cam = ctk.CTkComboBox(master=self,
                                            values=self.values_cam,
                                            variable=self.box_variable_cam,
                                            state='readonly',
                                            command=self.selected_option_cam)
        self.combobox_cam.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # self.combobox_cam.bind('<<ComboboxSelected>>', self.selected_option_cam)

        self.combobox_rob = ctk.CTkComboBox(master=self,
                                            values=self.values,
                                            variable=self.box_variable,
                                            state='readonly',
                                            command=self.selected_option)
        self.combobox_rob.grid(row=1, column=3, columnspan=3, padx=10, pady=10)

        # self.combobox_rob.bind('<<ComboboxSelected>>', self.selected_option)

        self.automated_calib = ctk.CTkButton(master=self,
                                             text='Auto Calibration',
                                             command=self.auto_calibration)
        self.automated_calib.grid(row=2, column=0, columnspan=3)

        CTkToolTip(self.automated_calib, message='For automated calibration you need\n'
                                                 'at least 20 predefined positions of the robot\n'
                                                 'and you must input them in the entry bellow')

        self.manual_calib = ctk.CTkButton(master=self,
                                          text='Manual Calibration',
                                          command=self.manual_calibration)
        self.manual_calib.grid(row=2, column=3, columnspan=4)
        CTkToolTip(self.manual_calib, message='For manual calibration you need\n'
                                              'at least 20 positions of the robot.\n'
                                              'Change the position of the robot and press '
                                              'Get Current Position')

        # self.entry_pose = ctk.CTkEntry(master=self)
        # self.entry_pose.grid(row=3, column=0, columnspan=7, rowspan=4, sticky='nswe')

        self.button_show_pic = ctk.CTkButton(master=self,
                                             text='Show Picture',
                                             command=self.show_pic)
        self.button_show_pic.grid(row=13, column=0, columnspan=3)

        self.button_show_depth = ctk.CTkButton(master=self,
                                               text='Show Depth map',
                                               command=self.show_depth)
        self.button_show_depth.grid(row=13, column=3, columnspan=4)

        self.background_image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self, image=self.background_image)
        self.label.grid(row=14, column=0, columnspan=7, rowspan=5)

    def connect_to_cam(self):
        if not self.connected_camera:
            try:
                app = zivid.Application()
                self.camera = app.connect_camera()
                self.connected_camera = True
                print('ok')
                if self.connected_camera:
                    # self.connect_cam_button.configure(fg_color='#F8C471')
                    messagebox.showinfo('Connected!', 'Camera is connected!')
                    self.combobox_cam.configure(state='normal')
                    # self.combobox_cam.bind('<<ComboboxSelected>>', self.selected_option_cam)

            except Exception:
                messagebox.showinfo('Error', 'You could not connect to the camera!\n'
                                                           'Check your network!')
                self.connected_camera = False

                if not self.connected_camera:
                    self.combobox_cam.configure(state='readonly')
                    CTkToolTip(self.combobox_cam, message='Since you are not connected to the camera\n'
                                                          'the options are only readable')

        else:
            messagebox.showinfo('Connected!', 'You are already connected to the camera!')

    def init_robot(self):
        if not self.connected_robot:
            try:
                self.robot_fanuc.connect()
                self.connected_robot = True
                print('robot ok')

                if self.connected_robot:
                    # self.button_rob.configure(fg_color='#F8C471')
                    messagebox.showinfo('Connected!', 'Robot is connected!')
                    self.combobox_rob.configure(state='normal')
                    # self.combobox_rob.bind('<<ComboboxSelected>>', self.selected_option)

            except Exception:
                messagebox.showinfo('Error!', 'You could not connect to the robot!\n'
                                              'Check your network!')
                self.connected_robot = False

                if not self.connected_robot:
                    self.combobox_rob.configure(state='readonly')
                    CTkToolTip(self.combobox_rob, message='Since you are not connected to the robot\n'
                                                          'the options are only readable')

        else:
            messagebox.showinfo('Connected!', 'You are already connected to the robot!')

    def selected_option(self, event):

        variable = self.box_variable.get()
        if variable == 'Get Current Pose':
            print(self.get_curr_pose())
        elif variable == 'Get Current JPose':
            print(self.robot_fanuc.get_curjpos())

    def selected_option_cam(self, event):

        variable = self.box_variable_cam.get()
        if variable == "Warm Up Cam":
            print('starting')
            print(warmup(self.camera))
        elif variable == 'Get Intrinsics':
            camera_intrinsics(self.camera)

    def auto_calibration(self):

        if not self.automated_calib_on:
            if self.manual_calib_on:
                self.manual_calib_get_pose_button.grid_forget()
                self.entry_curr_pose_show.grid_forget()

            self.entry_pose = ctk.CTkEntry(master=self)
            self.entry_pose.grid(row=3, column=0, columnspan=7, rowspan=3, sticky='nswe')

            self.take_pose_button = ctk.CTkButton(master=self,
                                                  text='Take positions',
                                                  command=self.take_positions)
            self.take_pose_button.grid(row=7, column=2, columnspan=2)

            self.automated_calib_on = True
            self.manual_calib_on = False

    def take_positions(self):
        try:
            variable = self.entry_pose.get().split(' ')
            print(variable)

            for i in variable:
                coordinate = [int(coord) for coord in i.split(',')]
                self.coordinates[variable.index(i)] = coordinate

            return_value = calibrate_hand_eye(robot=self.robot_fanuc,
                                              robot_joints=self.coordinates,
                                              camera=self.camera)

            # self.entry_pose.insert(0, return_value)
        except Exception:
            messagebox.showinfo('Error!', 'You either pressed the button with no positions inserted '
                                          'or there was some kind of error!')

    def manual_calibration(self):
        if not self.manual_calib_on:
            if self.automated_calib_on:
                self.entry_pose.grid_forget()
                self.take_pose_button.grid_forget()

            self.manual_calib_get_pose_button = ctk.CTkButton(master=self,
                                                              text='Get Current Pose',
                                                              command=self.get_curr_pose)
            self.manual_calib_get_pose_button.grid(row=3, column=2, columnspan=2)

            self.entry_curr_pose_show = ctk.CTkEntry(master=self)
            self.entry_curr_pose_show.grid(row=4, column=0, columnspan=7, sticky='nswe')

            self.manual_calib_on = True
            self.automated_calib_on = False

        # manual_calibrate_hand_eye(robot=self.robot_fanuc,
        #                           camera=self.camera)

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

        try:
            self.robot_fanuc.get_curpos = get_curposv2
            cur_pose = self.robot_fanuc.get_curpos(self.robot_fanuc, 8, 8)

        except Exception:
            messagebox.showinfo('Error!', 'Cannot get the robots position. Check '
                                          'the connection!')


cur_pose = None
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

App()