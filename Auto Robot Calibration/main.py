import logging
import threading
import customtkinter as ctk
from collections import deque
import multiprocessing

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
from entries import CamIPEntry, CamPortEntry, RobPortEntry, RobIPEntry, RobTFEntry, RobUFEntry
from frame_coords import FrameCoords
from CTkToolTip import *


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
        super().__init__() # With the super method we include a master

        self.title('Calibration App')
        self.width = 350
        self.height = 700
        self.x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        # self.maxsize(700, 700)
        self.minsize(700, 350)
        self.maxsize(700, 700)

        self.camera = None
        self.robot = None

        self.robot_button = None
        self.camera_button = None


        """
        Configuring Frames
        """
        self.MenuLeft = FrameLeft(self)
        self.MenuLeft.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        self.FrameCoords = FrameCoords(self.MenuLeft)
        self.FrameCoords.place(relx=0.05, rely=0.5, relwidth=0.90, relheight=0.2)

        # self.MenuRight = FrameRight(self)
        # self.MenuRight.place(relx=0.502, rely=0.01, relwidth=0.49, relheight=0.98)

        """
        Configuring Entries
        """
        self.CamIPEntry = CamIPEntry(self.MenuLeft)
        self.CamIPEntry.place(relx=0.05, rely=0.05)

        self.CamPortEntry = CamPortEntry(self.MenuLeft)
        self.CamPortEntry.place(relx=0.20, rely=0.05)

        self.RobIPEntry = RobIPEntry(self.MenuLeft)
        self.RobIPEntry.place(relx=0.55, rely=0.05)

        self.RobPortEntry = RobPortEntry(self.MenuLeft)
        self.RobPortEntry.place(relx=0.70, rely=0.05)

        self.RobUF = RobUFEntry(self.MenuLeft)
        self.RobUF.place(relx=0.55, rely=0.005)

        self.RobTF = RobTFEntry(self.MenuLeft)
        self.RobTF.place(relx=0.612, rely=0.005)

        """
        Configuring Buttons
        """
        self.RobotButton = RobotButton(self.MenuLeft)
        self.RobotButton.place(relx=0.55, rely=0.1)

        self.CameraButton = CameraButton(self.MenuLeft)
        self.CameraButton.place(relx=0.05, rely=0.1)

        self.CalibrateButton = CalibrateButton(self.MenuLeft)
        self.CalibrateButton.place(relx=0.35, rely=0.90)

        # self.FrameZivid = FrameZivid(self.MenuRight)
        # self.FrameZivid.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.79)

        self.WarmUp = WarmUpButton(self.MenuLeft)
        self.WarmUp.place(relx=0.15, rely=0.2)

        self.TakePicButton = TakePicButton(self.MenuLeft)
        self.TakePicButton.place(relx=0.15, rely=0.3)

        self.IntrscsButton = IntrButton(self.MenuLeft)
        self.IntrscsButton.place(relx=0.15, rely=0.4)
        # self.IntrscsButton.grid(row=3, column=1)

        self.CurrPose = CurrPoseButton(self.MenuLeft)
        self.CurrPose.place(relx=0.65, rely=0.2)

        self.CurrJPose = CurrJPoseButton(self.MenuLeft)
        self.CurrJPose.place(relx=0.65, rely=0.3)

        self.SendRobot = SendRobotButton(self.MenuLeft)
        self.SendRobot.place(relx=0.65, rely=0.4)

        """
        adding images to the GUI
        """
        self.ImageCam = ImageCam(self.MenuLeft)
        self.ImageCam.place(relx=0.34, rely=0.01)
        # Using .lift() function in order to bring the image
        # At the back of the button. It must be added
        # After the image is defined.
        self.CameraButton.lift()

        self.ImageRob = ImageRobot(self.MenuLeft)
        self.ImageRob.place(relx=0.85, rely=0.025)
        self.RobotButton.lift()

        self.ImageIntr = ImageIntr(self.MenuLeft)
        self.ImageIntr.place(relx=0.15, rely=0.4)

        self.CamButtonBlur = CamButtonBlur(self.MenuLeft)
        self.CamButtonBlur.place(relx=0.15, rely=0.3)

        self.WarmUpBlur = WarmUpBlur(self.MenuLeft)
        self.WarmUpBlur.place(relx=0.15, rely=0.2)

        self.CurrPoseBlur = CurrPoseBlur(self.MenuLeft)
        self.CurrPoseBlur.place(relx=0.65, rely=0.2)

        self.CurrJPoseBlur = CurrJPoseBlur(self.MenuLeft)
        self.CurrJPoseBlur.place(relx=0.65, rely=0.3)

        self.SendRobotBlur = SendRobotBlur(self.MenuLeft)
        self.SendRobotBlur.place(relx=0.65, rely=0.4)

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

            if que[0]:
                self.camera = que[1]
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

            if que_rob[0]:
                self.robot = que_rob[1]
                self.SendRobotBlur.place_forget()
                self.CurrPoseBlur.place_forget()
                self.CurrJPoseBlur.place_forget()
                self.Thread_robot_check_connection.start()

                    # Change Robot picture color
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
    # global robot
    # global camera

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

        # progress_bar_splash_scr = ctk.CTkProgressBar(master=splash_screen,
        #                                              orientation='horizontal',
        #                                              mode='indeterminate',
        #                                              length=100)
        # progress_bar_splash_scr.place(relx=0.1, rely=0.8)
        # progress_bar_splash_scr.lift()

        app = App()
        app.mainloop()

    except Exception as ex:
        logging.error(f"Window exception: {ex}")

