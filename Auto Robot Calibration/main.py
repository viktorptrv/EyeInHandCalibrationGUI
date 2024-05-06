import time
import tkinter as tk
import customtkinter as ctk

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


class App(ctk.CTk):
    def __init__(self):
        super().__init__() # With the super method we include a master

        self.title('Calibration App')
        self.geometry('700x350')
        # self.maxsize(700, 700)
        self.minsize(700, 700)

        self.robot_button = None
        self.camera_button = None

        """
        Configuring the Menus
        """
        self.MenuLeft = FrameLeft(self)
        self.MenuLeft.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

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
        self.CameraButton.configure(command=lambda: self.WarmUpBlur.place_forget())


if __name__ == '__main__':
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')

    """
    First we create the object and then we run it with mainloop.
    This way it will create all the needed widgets and run all the threads
    """
    app = App()
    app.mainloop()
