import tkinter as tk
import customtkinter as ctk
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
        self.calibration = None
        self.geometry('1300x500')
        self.maxsize(1300, 600)
        self.minsize(1300, 600)

        # Add widgets
        self.MiddleMenuTop = MiddleMenuTop(self)
        self.TopMenu = TopMenu(self)
        self.MiddleMenuMid = MiddleMenuMid(self)
        # self.MiddleMenuBottom = MiddleMenuBottom(self)
        self.RightMenuTop = RightMenuTop(self)
        # self.RightMenuMid = RightMenuMid(self)
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

        self.TopMenuFrameOne = RobotFrame(self)
        self.CalibrationFrame = CalibrationFrame(self)

        self.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.9)


class RobotFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.connected_robot = False
        self.connected_camera = False

        self.robot_fanuc = Robot(
                                robot_model="LHMROB011",
                                host="10.37.115.206",
                                port=18735,
                                ee_DO_type="RDO",
                                ee_DO_num=7)

        self.combobox = None
        self.values = ['Choose an Option', 'Get Current Pose', 'Get Current JPose']
        self.box_variable = tk.StringVar(value=self.values[0])
        self.camera = None
        self.button_rob = None
        self.button_cam = None
        self.button_pose = None
        self.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.4)

        self.create_widgets()

    def create_widgets(self):
        self.button_rob = ctk.CTkButton(master=self,
                                        text='Connect to Robot',
                                        command=self.init_robot)
        self.button_rob.pack(pady=20, padx=10, side='top')

        self.combobox = ctk.CTkComboBox(master=self,
                                        values=self.values,
                                        variable=self.box_variable,
                                        state='readonly')
        self.combobox.pack(pady=10, padx=10, side='top')

        self.button_cam = ctk.CTkButton(master=self,
                                        text='Connect to Camera',
                                        command=self.connect_to_cam)
        self.button_cam.pack(pady=10, padx=10, side='top')

    def connect_to_cam(self):
        if not self.connected_camera:
            try:
                app = zivid.Application()
                self.camera = app.connect_camera()
                self.connected_camera = True
            except Exception:
                messagebox.showinfo('Error', 'You could not connect to the camera!\n'
                                             'Check your network!')
                self.connected_camera=False

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


class CalibrationFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4)
        self.list = []
        self.pose_entry = None
        self.manual_calib = None
        self.automated_calib = None

        self.widgets()

    def widgets(self):
        self.automated_calib = ctk.CTkButton(master=self,
                                             text='Auto Calibration',
                                             command=self.auto_calibration)
        self.automated_calib.pack(pady=35, padx=10, side='top')

        self.automated_calib.bind('<Button-1>', self.auto_calibration)

        CTkToolTip(self.automated_calib, message='For automated calibration you need\n'
                                                 'at least 20 predefined positions of the robot\n'
                                                 'and you must input them in the menu')

        self.manual_calib = ctk.CTkButton(master=self,
                                          text='Manual Calibration',
                                          command=self.manual_calibration)
        self.manual_calib.pack(pady=10, padx=10, side='top')
        CTkToolTip(self.manual_calib, message='For manual calibration you need\n'
                                              'at least 20 positions of the robot.\n'
                                              'Change the position of the robot and press'
                                              'Get Current Position')

    def auto_calibration(self):
        pass

    def manual_calibration(self):
        pass


class MiddleMenuTop(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.23, rely=0.02, relwidth=0.35, relheight=0.3)
        self.entry_pose = None
        self.label=None

        self.activate_widget()

    def activate_widget(self):
        self.label = ctk.CTkLabel(master=self,
                                  text='Automated Calibration Input')
        self.label.pack(padx=10, pady=0.5, fill='both', expand=True)

        self.entry_pose = ctk.CTkEntry(master=self)
        self.entry_pose.pack(padx=5, pady=10, fill='both', expand=True)
        if calibration:
            self.entry_pose.configure(state='enabled')
        print('ok')


class MiddleMenuMid(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0.23, rely=0.325, relwidth=0.35, relheight=0.3)


class RightMenuTop(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = None
        self.frame_buttons = None
        self.button_show_pic= None
        self.button_show_depth = None
        self.place(relx=0.585, rely=0.02, relwidth=0.4, relheight=0.906)
        self.image = Image.open("dark_python.png")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.frame_buttons = ctk.CTkFrame(master=self)
        self.frame_buttons.pack(pady=5, padx=10, fill='both', expand=True)

        self.label = tk.Label(self, image=self.background_image)
        self.label.pack(padx=5, pady=8, fill='both', expand=True)
        self.label.bind('<Configure>', self._resize_image)

        self.activate_widgets()

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.background_image)

    def activate_widgets(self):
        self.button_show_pic = ctk.CTkButton(master=self.frame_buttons,
                                             text='Show Picture',
                                             command=self.show_pic)
        self.button_show_pic.pack(padx=60, pady=5, side='left')

        self.button_show_depth = ctk.CTkButton(master=self.frame_buttons,
                                               text='Show Depth map',
                                               command=self.show_depth)
        self.button_show_depth.pack(padx=60, pady=5, side='right')

    def show_depth(self):
        pass

    def show_pic(self):
        pass


calibration = False

cur_pose = None
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
# Running the app
App()
