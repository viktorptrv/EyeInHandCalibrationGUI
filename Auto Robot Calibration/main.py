import logging
import threading
import customtkinter as ctk
from tkinter import ttk

import multiprocessing

from tkinter import filedialog as fd
from collections import deque
from tkinter import messagebox
from PIL import Image, ImageTk
from robot_button import RobotButton
from Menu_One import FrameLeft
from Menu_Two import FrameRight
from camera_button import CameraButton
from calibrate_button import CalibrateButton
from current_pose import CurrPoseButton
from curr_j_pose import CurrJPoseButton
from Intrinsics import IntrButton
from send_robot import SendRobotButton
from take_picture_button import TakePicButton
from warm_up import WarmUpButton
from images import ImageCam, ImageRobot, ImageIntr, CamButtonBlur, WarmUpBlur
from images import CurrPoseBlur, CurrJPoseBlur, SendRobotBlur
from zivid_image import FrameZivid
from entries import *
from frame_coords import FrameCoords
from choose_calibration import *
from coordinates_widgets import Coords, JCoords
from load_file_button import LoadFileButton
from text_poses import TextPoses
from CTkToolTip import *
from calibration_functions import calibrate_hand_eye, manual_calibrate_hand_eye
from menu_bar import MenuBar


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Petrov Engineering")

        self.height = 350
        self.width = 350
        self.x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

        self.overrideredirect(True)

        self.SplashLabel = ctk.CTkLabel(self,
                                        text='',
                                        image=ctk.CTkImage(light_image=Image.open('Images/logo-color.png'),
                                                           dark_image=Image.open('Images/logo-color.png'),
                                                           size=(self.width, self.height)))

        self.SplashLabel.pack(fill='both', expand=True)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()  # With the super method we include a master

        self.title('Calibration App')
        self.width = 700
        self.height = 700
        self.x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        # self.maxsize(700, 700)
        self.minsize(700, 350)
        # self.maxsize(700, 700)

        self.camera = None
        self.robot = None

        self.robot_button = None
        self.camera_button = None

        self.file_types = (('text files', '*.txt'),
                           ('All files', '*.*'))

        self.auto_calib_pose_dict = {}

        self.file_int = []

        self.calibration_type = None

        """
        Configuring Frames
        """
        self.Menu = FrameLeft(self)
        self.Menu.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        self.FrameCoords = FrameCoords(self.Menu)
        self.FrameCoords.place(relx=0.1, rely=0.5, relwidth=0.80, relheight=0.2)

        """
        Configuring Entries
        """
        self.CamIPEntry = CamIPEntry(self.Menu)
        self.CamIPEntry.place(relx=0.05, rely=0.05)

        self.CamPortEntry = CamPortEntry(self.Menu)
        self.CamPortEntry.place(relx=0.20, rely=0.05)

        self.RobIPEntry = RobIPEntry(self.Menu)
        self.RobIPEntry.place(relx=0.55, rely=0.05)

        self.RobPortEntry = RobPortEntry(self.Menu)
        self.RobPortEntry.place(relx=0.70, rely=0.05)

        self.RobUF = RobUFEntry(self.Menu)
        self.RobUF.place(relx=0.55, rely=0.005)

        self.RobTF = RobTFEntry(self.Menu)
        self.RobTF.place(relx=0.612, rely=0.005)

        self.Coords = Coords(self.FrameCoords)
        self.Coords.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.3)

        self.JCoords = JCoords(self.FrameCoords)
        self.JCoords.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.3)

        """
        Configuring Buttons
        """
        self.MenuBar = MenuBar(self)

        self.RobotButton = RobotButton(self.Menu)
        self.RobotButton.place(relx=0.55, rely=0.1)

        self.CameraButton = CameraButton(self.Menu)
        self.CameraButton.place(relx=0.05, rely=0.1)

        self.CalibrateButton = CalibrateButton(self.Menu)
        self.CalibrateButton.place(relx=0.35, rely=0.90)

        # self.FrameZivid = FrameZivid(self.MenuRight)
        # self.FrameZivid.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.79)

        self.WarmUp = WarmUpButton(self.Menu)
        self.WarmUp.place(relx=0.1, rely=0.2)

        self.TakePicButton = TakePicButton(self.Menu)
        self.TakePicButton.place(relx=0.1, rely=0.3)

        self.IntrscsButton = IntrButton(self.Menu)
        self.IntrscsButton.place(relx=0.1, rely=0.4)

        self.CurrPose = CurrPoseButton(self.Menu)
        self.CurrPose.place(relx=0.6, rely=0.2)

        self.CurrJPose = CurrJPoseButton(self.Menu)
        self.CurrJPose.place(relx=0.6, rely=0.3)

        self.SendRobot = SendRobotButton(self.Menu)
        self.SendRobot.place(relx=0.6, rely=0.4)

        self.AutoCalib_button = AutoCalibrate(self.FrameCoords)
        self.AutoCalib_button.place(relx=0.15, rely=0.05)
        # self.AutoCalib_button.configure(command=self.auto_checkbox_event)
        # self.AutoCalib_button.configure(state='disabled')
        self.AutoCalib_button.configure(state='normal')
        self.AutoCalib_button.configure(command=self.import_file_with_poses)

        self.ManualCalib_button = ManualCalibrate(self.FrameCoords)
        self.ManualCalib_button.place(relx=0.6, rely=0.05)
        self.ManualCalib_button.configure(command=self.man_checkbox_event)
        # self.ManualCalib_button.configure(state='disabled')
        self.ManualCalib_button.configure(state='normal')

        self.LoadFileButton = LoadFileButton(self.FrameCoords)

        self.TextPoses = TextPoses(self.FrameCoords)    # Holder for the poses
        
        self.EtH = EyeToHand(self.Menu)
        self.EtH.place(relx=0.37, rely=0.75)
        self.EtH.configure(command=self.eth_calib_type_checkbox)

        self.EiH = EyeInHand(self.Menu)
        self.EiH.place(relx=0.37, rely=0.8)
        self.EiH.configure(command=self.eih_calib_type_checkbox)

        """
        adding images to the GUI
        """
        self.ImageCam = ImageCam(self.Menu)
        self.ImageCam.place(relx=0.34, rely=0.01)
        # Using .lift() function in order to bring the image
        # At the back of the button. It must be added
        # After the image is defined.
        self.CameraButton.lift()

        self.ImageRob = ImageRobot(self.Menu)
        self.ImageRob.place(relx=0.85, rely=0.025)
        self.RobotButton.lift()

        self.ImageIntr = ImageIntr(self.Menu)
        self.ImageIntr.place(relx=0.1, rely=0.4)

        self.CamButtonBlur = CamButtonBlur(self.Menu)
        self.CamButtonBlur.place(relx=0.1, rely=0.3)

        self.WarmUpBlur = WarmUpBlur(self.Menu)
        self.WarmUpBlur.place(relx=0.1, rely=0.2)

        self.CurrPoseBlur = CurrPoseBlur(self.Menu)
        self.CurrPoseBlur.place(relx=0.6, rely=0.2)

        self.CurrJPoseBlur = CurrJPoseBlur(self.Menu)
        self.CurrJPoseBlur.place(relx=0.6, rely=0.3)

        self.SendRobotBlur = SendRobotBlur(self.Menu)
        self.SendRobotBlur.place(relx=0.6, rely=0.4)

        """
        За функциолността на бутоните, ще ги включим тук в отделна функция за всеки бутон
        """
        self.CameraButton.configure(command=self.thread_connect_camera)

        self.RobotButton.configure(command=self.thread_connect_robot)

        """
        Thread, който постоянно проверява дали има връзка с камерата/робота, след като са били свързани
        """
        self.Thread_robot_check_connection = threading.Thread(target=self.check_robot_connection, daemon=True)
        self.Thread_camera_check_connection = threading.Thread(target=self.check_camera_connection, daemon=True)
        # self.Thread_check_button = threading.Thread(target=self.enable_check_button, daemon=True)

    def eih_calib_type_checkbox(self):
        if self.EiH.get() == 1:
            self.EtH.configure(state='disable')
            self.calibration_type = 'eih'
        elif self.EiH.get() == 0:
            self.EtH.configure(state='normal')
            self.calibration_type = ''

    def eth_calib_type_checkbox(self):
        if self.EtH.get() == 1:
            self.EiH.configure(state='disable')
            self.calibration_type = 'eth'
        elif self.EtH.get() == 0:
            self.EiH.configure(state='normal')
            self.calibration_type = ''

    def import_file_with_poses(self):
        self.JCoords.place_forget()
        self.Coords.place_forget()
        if self.AutoCalib_button.check_var_auto.get() == 1:
            self.ManualCalib_button.configure(state='disabled')
            self.LoadFileButton.place(relx=0.35, rely=0.3)
            self.LoadFileButton.configure(command=self.load_file)
        else:
            self.ManualCalib_button.configure(state='normal')
            self.JCoords.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.3)
            self.Coords.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.3)
            if self.LoadFileButton:
                self.LoadFileButton.place_forget()
                self.TextPoses.place_forget()

    def load_file(self):
        self.TextPoses.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.35)
        try:
            file = fd.askopenfile(filetypes=self.file_types,
                                  initialdir="D:/Downloads")

            file_read = file.readlines()

            for i in range(len(file_read)):
                line = file_read[i].split(', ')
                last_index = line.pop(-1).strip('\n')
                self.file_int.append([int(i) for i in line])
                self.file_int[i].append(int(last_index))
                print(self.file_int)

            self.TextPoses.insert('1.0', file_read)

            for i in range(len(self.file_int)):
                self.auto_calib_pose_dict[i] = self.file_int[i]

            print(self.auto_calib_pose_dict)

        except Exception as ex:
            messagebox.showerror("Error!", "Could not read the file correctly!")

        try:
            if self.camera and self.robot:
                try:
                    if self.auto_calib_pose_dict:
                        calibrate_hand_eye(self.auto_calib_pose_dict,
                                           self.robot,
                                           self.camera)

                except Exception as ex:
                    messagebox.showwarning('Error!',
                                           'Could not find poses')

        except Exception as ex:
            messagebox.showwarning("Not connected!",
                                   "Either the camera or the robot is not connected!")
    # def enable_check_button(self):
    #     while self.camera and self.robot:
    #         self.AutoCalib_button.configure(state='normal')
    #         self.ManualCalib_button.configure(state='normal')

    # self.ManualCalib_button.configure(state='disabled')
    # self.AutoCalib_button.configure(state='disabled')

    # def auto_checkbox_event(self):
    # if self.AutoCalib_button.check_var_auto.get() == 1:
    #     self.ManualCalib_button.configure(state='disabled')
    # else:
    #     self.ManualCalib_button.configure(state='normal')

    def man_checkbox_event(self):
        if self.ManualCalib_button.check_var_manual.get() == 1:
            self.AutoCalib_button.configure(state='disabled')
        else:
            self.AutoCalib_button.configure(state='normal')

    def check_camera_connection(self):
        if not self.camera:
            messagebox.showwarning("Error!", "Camera is not connected")

    def check_robot_connection(self):
        if not self.robot:
            messagebox.showwarning("Error!", "Robot is not connected")

    def thread_connect_camera(self):
        # The deque class can be used for returning values
        # The deque class is thread safe and is iterable
        # A deque object does not block, if the maxsize has been reached.
        # In this case the last or first element is dropped from the list.
        que = deque()
        # Call work function
        try:
            t1 = threading.Thread(target=self.CameraButton.connect_camera(que))
            t1.start()

            # if que[0]:
            #     self.camera = que[1]
            #     self.WarmUpBlur.place_forget()
            #     self.ImageIntr.place_forget()
            #     self.CamButtonBlur.place_forget()
            #     self.Thread_camera_check_connection.start()
            #
            #     self.ImageCam.configure(image=ctk.CTkImage(light_image=Image.open('Images/camera_light_green.png'),
            #                             dark_image=Image.open('Images/camera_light_green.png'),
            #                             size=(100, 100)))
            #
            #     self.CamIPEntry.configure(fg_color='#2DFE54')
            #     self.CamPortEntry.configure(fg_color='#2DFE54')
            #     self.CameraButton.configure(fg_color='#2DFE54')
            #     self.CameraButton.configure(text="Camera Connected!")

            self.WarmUpBlur.place_forget()
            self.ImageIntr.place_forget()
            self.CamButtonBlur.place_forget()
            self.Thread_camera_check_connection.start()

            self.ImageCam.configure(image=ctk.CTkImage(light_image=Image.open('Images/camera_light_green.png'),
                                                       dark_image=Image.open('Images/camera_light_green.png'),
                                                       size=(100, 100)))

            self.CamIPEntry.configure(fg_color='#2DFE54')
            self.CamPortEntry.configure(fg_color='#2DFE54')
            self.CameraButton.configure(fg_color='#2DFE54')
            self.CameraButton.configure(text="Camera Connected!")

        except Exception as ex:
            print(f"Camera exception: {ex}")
            logging.error(f"Camera Exception: {ex}")

    def thread_connect_robot(self):
        # The queue class can be used for returning values
        que_rob = deque()
        # Call work function
        try:
            t2 = threading.Thread(target=self.RobotButton.connect_robot(que_rob), daemon=True)
            t2.start()

            # if que_rob[0]:
            #     self.robot = que_rob[1]
            #     self.SendRobotBlur.place_forget()
            #     self.CurrPoseBlur.place_forget()
            #     self.CurrJPoseBlur.place_forget()
            #     self.Thread_robot_check_connection.start()
            #
            #     self.ImageRob.configure(image=ctk.CTkImage(light_image=Image.open('Images/robotic_arm_green.png'),
            #                             dark_image=Image.open('Images/robotic_arm_green.png'),
            #                             size=(80, 80)))
            #
            #     self.RobUF.configure(fg_color='#2DFE54')
            #     self.RobotButton.configure(fg_color='#2DFE54')
            #     self.RobTF.configure(fg_color='#2DFE54')
            #     self.RobIPEntry.configure(fg_color='#2DFE54')
            #     self.RobPortEntry.configure(fg_color='#2DFE54')
            #     self.RobotButton.configure(text="Robot Connected!")

            self.SendRobotBlur.place_forget()
            self.CurrPoseBlur.place_forget()
            self.CurrJPoseBlur.place_forget()
            self.Thread_robot_check_connection.start()

            self.ImageRob.configure(image=ctk.CTkImage(light_image=Image.open('Images/robotic_arm_green.png'),
                                                       dark_image=Image.open('Images/robotic_arm_green.png'),
                                                       size=(80, 80)))

            self.RobUF.configure(fg_color='#2DFE54')
            self.RobotButton.configure(fg_color='#2DFE54')
            self.RobTF.configure(fg_color='#2DFE54')
            self.RobIPEntry.configure(fg_color='#2DFE54')
            self.RobPortEntry.configure(fg_color='#2DFE54')
            self.RobotButton.configure(text="Robot Connected!")

        except Exception as ex:
            print(f"Robot exception: ", ex)
            logging.error(f"Robot Exception: {ex}")


if __name__ == '__main__':
    def run_window():
        splash_screen.destroy()


    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    """
    First we create the object and then we run it with mainloop.
    This way it will create all the needed widgets and run all the threads
    """
    try:
        splash_screen = SplashScreen()
        splash_screen.after(3000, run_window)
        splash_screen.mainloop()

        app = App()
        app.mainloop()

    except Exception as ex:
        logging.error(f"Window exception: {ex}")
