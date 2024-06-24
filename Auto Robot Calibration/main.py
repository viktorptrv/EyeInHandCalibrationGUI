import logging
import os
from pathlib import Path

import sys
import zivid
import threading
import numpy as np
from tkinter import filedialog as fd
from collections import deque
from tkinter import messagebox
from PIL import Image, ImageTk

from Menu_One import FrameLeft
from robot_button import RobotButton
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
from entries import *
from frame_coords import FrameCoords
from choose_calibration import *
from coordinates_widgets import Coords, JCoords
from load_file_button import LoadFileButton
from text_poses import TextPoses
from CTkToolTip import *
from calibration_functions import calibrate_hand_eye, _assisted_capture, \
    _perform_calibration
from menu_bar import MenuBar
from zivid_functions import warmup, get_camera_intrinsics
from zivid_functions.sample_utils import save_load_matrix
import functions_for_calibration
import subprocess


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

        self.rob_uf = None
        self.rob_tf = None

        self.file_types = (('text files', '*.txt'),
                           ('All files', '*.*'))

        self.auto_calib_pose_dict = {}

        self.file_int = []

        self.calibration_type = None
        self.manual_calib_label = None
        self.current_pose_id = 0
        self.handeye_input = []

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
        self.CamIPEntry.configure(text_color='black')

        self.CamPortEntry = CamPortEntry(self.Menu)
        self.CamPortEntry.place(relx=0.20, rely=0.05)
        self.CamPortEntry.configure(text_color='black')

        self.RobIPEntry = RobIPEntry(self.Menu)
        self.RobIPEntry.place(relx=0.55, rely=0.05)

        self.RobPortEntry = RobPortEntry(self.Menu)
        self.RobPortEntry.place(relx=0.70, rely=0.05)

        self.RobUF = RobUFEntry(self.Menu)
        self.RobUF.place(relx=0.55, rely=0.005)

        self.RobTF = RobTFEntry(self.Menu)
        self.RobTF.place(relx=0.612, rely=0.005)

        self.RobUF.configure(text_color='black')
        self.RobTF.configure(text_color='black')
        self.RobIPEntry.configure(text_color='black')
        self.RobPortEntry.configure(text_color='black')

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
        self.CalibrateButton.configure(command=self.start_calibration)

        self.WarmUp = WarmUpButton(self.Menu)
        self.WarmUp.place(relx=0.1, rely=0.2)
        self.WarmUp.configure(command=self.warm_up_function)

        self.TakePicButton = TakePicButton(self.Menu)
        self.TakePicButton.place(relx=0.1, rely=0.3)

        self.IntrscsButton = IntrButton(self.Menu)
        self.IntrscsButton.place(relx=0.1, rely=0.4)
        self.IntrscsButton.configure(command=self.cam_intr)

        self.CurrPose = CurrPoseButton(self.Menu)
        self.CurrPose.place(relx=0.6, rely=0.2)
        self.CurrPose.configure(command=self.get_current_position)

        self.CurrJPose = CurrJPoseButton(self.Menu)
        self.CurrJPose.place(relx=0.6, rely=0.3)
        self.CurrPose.configure(command=self.get_currJpose)

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

        self.TextPoses = TextPoses(self.FrameCoords)  # Holder for the poses

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
        # self.Thread_Ready_Calibration = multiprocessing.Process(target=self.ready_calibration, daemon=True)
        # self.Thread_Ready_Calibration.start()
        # self.Thread_Ready_Calibration.join()
        # self.Thread_check_button = threading.Thread(target=self.enable_check_button, daemon=True)

    # def ready_calibration(self):
    #     while True:
    #         if self.camera and self.robot:
    #             if self.calibration_type == 'eih' and self.auto_calib_pose_dict:
    #                 self.CalibrateButton.configure(state="normal")
    #                 self.CalibrateButton.configure(fg_color='#2DFE54')
    #                 self.CalibrateButton.configure(command=self.calibrate_eye_in_hand)
    #             elif self.calibration_type == 'eth':
    #                 self.CalibrateButton.configure(state="normal")
    #                 self.CalibrateButton.configure(fg_color='#2DFE54')
    #                 self.CalibrateButton.configure(command=self.calibrate_eye_to_hand)

    def calibrate_eye_in_hand(self):
        calibrate_hand_eye(self.auto_calib_pose_dict,
                           self.robot,
                           self.camera,
                           self.calibration_type)

    def calibrate_eye_to_hand(self):
        # manual_calibrate_hand_eye(self.robot,
        #                           self.camera)
        pass

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
                self.file_int.append([float(i) for i in line])
                self.file_int[i].append(float(last_index))
                print(self.file_int)

            self.TextPoses.insert('1.0', file_read)

            for i in range(len(self.file_int)):
                self.auto_calib_pose_dict[i] = self.file_int[i]

            if len(self.auto_calib_pose_dict) < 20:
                result = messagebox.askyesno("Positions", 'The number of positions are less than '
                                                          '20\nAre you sure you want to continue?')
                print(result)
                if result:
                    if self.camera and self.robot:
                        self.CalibrateButton.configure(state='normal')
                        self.CalibrateButton.configure(fg_color='#2DFE54')

                else:
                    if self.CalibrateButton.state == 'normal':
                        self.CalibrateButton.configure(fg_color='#ffba33')
                        self.CalibrateButton.configure(text_color='black')
                        self.CalibrateButton.configure(state='disable')
                    self.auto_calib_pose_dict.clear()
                    self.file_int.clear()
                    self.TextPoses.delete('1.0', 'end')
                    print(self.auto_calib_pose_dict)


    # def enable_check_button(self):
    #     while self.camera and self.robot:
    #         self.AutoCalib_button.configure(state='normal')
    #         self.ManualCalib_button.configure(state='normal')

    # self.ManualCalib_button.configure(state='disabled')
    # self.AutoCalib_button.configure(state='disabled')

    def man_checkbox_event(self):
        if self.ManualCalib_button.check_var_manual.get() == 1:
            self.AutoCalib_button.configure(state='disabled')

            self.JCoords.forget_widgets()

            self.manual_calib_label = ctk.CTkLabel(master=self.JCoords,
                                                   text='Press Current Pose button.')
            self.manual_calib_label.place(relx=0.33, rely=0.1)
        else:
            self.AutoCalib_button.configure(state='normal')
            if self.manual_calib_label:
                self.manual_calib_label.place_forget()
                self.JCoords.place_widget()

    def check_camera_connection(self):
        if not self.camera:
            messagebox.showwarning("Error!", "Camera is not connected")

    def check_robot_connection(self):
        if not self.robot:
            messagebox.showwarning("Error!", "Robot is not connected")

    def connect_to_camera(self, que):
        que_return = CameraButton.connect_camera(que)

        if que_return[0]:
            self.camera = que_return[1]
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
            self.CamIPEntry.configure(fg_color='#2DFE54')
            self.CamPortEntry.configure(fg_color='#2DFE54')

    def thread_connect_camera(self):
        """
        The deque class can be used for returning values
        The deque class is thread safe and is iterable
        A deque object does not block, if the maxsize has been reached.
        In this case the last or first element is dropped from the list.
        """
        que_cam = deque()
        try:
            if not(self.CamIPEntry.get() and self.CamPortEntry.get()):
                question = messagebox.askyesno("Continue?", "There was no IP or Port input. Is the camera\n"
                                                 "in the same network as the PC?")
                if question == 'yes':
                    self.connect_to_camera(que_cam)

            if self.CamIPEntry.get():
                cam_ip = self.CamIPEntry.get()
                with open('cam_config.txt', 'a') as file:
                    file.write(f'Camera IP = {cam_ip}\n')
            else:
                try:
                    with open('cam_config.txt') as file:
                        for line in file:
                            if line.startswith('Camera IP ='):
                                cam_ip = line.split('=')[1].strip()
                                break
                        if not cam_ip:
                            messagebox.showerror('Error', 'Camera IP not found in the config file.\n'
                                                          'Input IP')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    cam_ip = None
                    messagebox.showerror('Error', 'Check logging file for the error!')

            if self.CamPortEntry.get():
                cam_port = self.CamPortEntry.get()
                with open('cam_config.txt', 'a') as file:
                    file.write(f'Camera Port = {cam_port}\n')
            else:
                try:

                    with open('cam_config.txt') as file:
                        for line in file:
                            if line.startswith('Camera Port ='):
                                cam_port = line.split('=')[1].strip()
                                self.CamPortEntry.insert('1.0', cam_port)
                                break
                        if not cam_port:
                            messagebox.showerror('Error', 'Camera IP not found in the config file.\n'
                                                          'Input IP')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    cam_port = None
                    messagebox.showerror('Error', 'Check logging file for the error!')



            # self.WarmUpBlur.place_forget()
            # self.ImageIntr.place_forget()
            # self.CamButtonBlur.place_forget()
            # self.Thread_camera_check_connection.start()
            #
            # self.ImageCam.configure(image=ctk.CTkImage(light_image=Image.open('Images/camera_light_green.png'),
            #                                            dark_image=Image.open('Images/camera_light_green.png'),
            #                                            size=(100, 100)))
            #
            # self.CameraButton.configure(fg_color='#2DFE54')
            # self.CameraButton.configure(text="Camera Connected!")

        except Exception as exceptionmsg:
            print(f"Camera exception: {exceptionmsg}")
            logging.error(f"Camera Exception: {exceptionmsg}")

    def thread_connect_robot(self):

        # The queue class can be used for returning values
        que_rob = deque()
        # Call work function
        try:
            if self.RobIPEntry.get():
                rob_ip = self.RobIPEntry.get()
                with open('rob_config.txt', 'a') as file:
                    file.write(f'Robot IP = {rob_ip}\n')
            else:
                try:
                    with open('rob_config.txt') as file:
                        for line in file:
                            if line.startswith('Robot IP ='):
                                rob_ip = line.split('=')[1].strip()
                                break
                        if not rob_ip:
                            messagebox.showerror('Error', 'Robot IP not found in the config file.\n'
                                                          'Input IP')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    rob_ip = None
                    messagebox.showerror('Error', 'No information for robot ip')

            if self.RobPortEntry.get():
                rob_port = self.RobPortEntry.get()
                with open('rob_config.txt', 'a') as file:
                    file.write(f'Robot Port = {rob_port}\n')
            else:
                try:
                    with open('rob_config.txt') as file:
                        for line in file:
                            if line.startswith('Robot Port ='):
                                rob_port = line.split('=')[1].strip()
                                break
                        if not rob_port:
                            messagebox.showerror('Error', 'Robot Port not found in the config file.\n'
                                                          'Input Port')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    rob_port = None
                    messagebox.showerror('Error', 'No information for robot port')

            if self.RobUF.get():
                self.rob_uf = self.RobUF.get()
                with open('rob_config.txt', 'a') as file:
                    file.write(f'Robot UF = {self.rob_uf}\n')
            else:
                try:
                    with open('rob_config.txt') as file:
                        for line in file:
                            if line.startswith('Robot UF ='):
                                self.rob_uf = line.split('=')[1].strip()
                                break

                        if not self.rob_uf:
                            messagebox.showerror('Error', 'Robot UF not found in the config file.\n'
                                                          'Input UF')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    self.rob_uf = None
                    messagebox.showerror('Error', 'No information for robot uf')

            if self.RobTF.get():
                self.rob_tf = self.RobTF.get()
                with open('rob_config.txt', 'a') as file:
                    file.write(f'Robot TF = {self.rob_tf}\n')
            else:
                try:

                    with open('rob_config.txt') as file:
                        for line in file:
                            if line.startswith('Robot TF ='):
                                self.rob_tf = line.split('=')[1].strip()
                                break
                        if not self.rob_tf:
                            messagebox.showerror('Error', 'Robot TF not found in the config file.\n'
                                                          'Input TF')

                except Exception as exceptionmsg:
                    logging.error(str(exceptionmsg))
                    self.rob_tf = None
                    messagebox.showerror('Error', 'No information for robot tf')

            t2 = threading.Thread(target=self.RobotButton.connect_robot(que_rob, rob_ip, rob_port), daemon=True)
            t2.start()
            if que_rob[0]:
                self.robot = que_rob[1]
                self.robot.get_curpos = self.get_curposev2(self.rob_uf, self.rob_tf)
                self.SendRobotBlur.place_forget()
                self.CurrPoseBlur.place_forget()
                self.CurrJPoseBlur.place_forget()
                self.Thread_robot_check_connection.start()

                self.ImageRob.configure(image=ctk.CTkImage(light_image=Image.open('Images/robotic_arm_green.png'),
                                                           dark_image=Image.open('Images/robotic_arm_green.png'),
                                                           size=(80, 80)))

                self.RobotButton.configure(fg_color='#2DFE54')
                self.RobotButton.configure(text="Robot Connected!")

                self.RobUF.configure(fg_color='#2DFE54')
                self.RobTF.configure(fg_color='#2DFE54')
                self.RobIPEntry.configure(fg_color='#2DFE54')
                self.RobPortEntry.configure(fg_color='#2DFE54')

        except Exception as exceptionmsg:
            print(f"Robot exception: ", exceptionmsg)
            logging.error(f"Robot Exception: {exceptionmsg}")

    @staticmethod
    def get_curposev2(uframe, tframe) -> list[float]:
        """
        Gets current cartesian position of tool center point.

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

    def get_current_position(self):
        try:
            if (self.Coords.Entry1 or
                    self.Coords.Entry2 or
                    self.Coords.Entry3 or
                    self.Coords.Entry4 or
                    self.Coords.Entry5 or
                    self.Coords.Entry6):
                self.Coords.Entry1.delete('1.0', 'end')
                self.Coords.Entry2.delete('1.0', 'end')
                self.Coords.Entry3.delete('1.0', 'end')
                self.Coords.Entry4.delete('1.0', 'end')
                self.Coords.Entry5.delete('1.0', 'end')
                self.Coords.Entry6.delete('1.0', 'end')

            vals = self.robot.get_curpose()
            x, y, z, w, r, p = vals[0], vals[2], vals[3], vals[4], vals[5], vals[6]
            self.Coords.Entry1.insert('1.0', x)
            self.Coords.Entry2.insert('1.0', y)
            self.Coords.Entry3.insert('1.0', z)
            self.Coords.Entry4.insert('1.0', w)
            self.Coords.Entry5.insert('1.0', r)
            self.Coords.Entry6.insert('1.0', p)

            if self.ManualCalib_button.check_var_manual.get() == 1:
                if self.current_pose_id <= 20:
                    try:
                        matrix = functions_for_calibration.create_4x4_matrix(float(x),
                                                                             float(y),
                                                                             float(z),
                                                                             float(w),
                                                                             float(r),
                                                                             float(p))

                        matrix_string = functions_for_calibration.matrix_to_string(matrix)

                        elements = matrix_string.split(maxsplit=15)
                        data = np.array(elements, dtype=np.float64).reshape((4, 4))
                        robot_pose = zivid.calibration.Pose(data)
                        print(f"The following pose was entered:\n{robot_pose}")

                        with open("PosesManual.txt", 'a') as file:
                            file.write(f"Pose with index {self.current_pose_id}: {x}, {y}, {z}, {r}, {p}, {w}")

                        frame = _assisted_capture(self.camera, self.current_pose_id)

                        detection_result = zivid.calibration.detect_feature_points(frame.point_cloud())

                        if detection_result.valid():
                            print("Calibration board detected")
                            self.handeye_input.append(zivid.calibration.HandEyeInput(robot_pose, detection_result))
                            self.current_pose_id += 1
                        else:
                            messagebox.showinfo('Not that bad of an Error', "Failed to detect calibration"
                                                                            " board, ensure that the entire board is "
                                                                            "in the view of the camera")
                    except Exception as exceptionmsg:
                        messagebox.showinfo('Error', "Failed to add pose")

                if self.current_pose_id == 20:
                    messagebox.showinfo("Enought Poses", "You have enough poses and pictures\n"
                                                         "You can start the calibration")

                    # calibration_result = _perform_calibration(self.handeye_input, self.calibration_type)
                    # transform = calibration_result.transform()
                    # transform_file_path = Path(Path(__file__).parent / "CalibrationMatrixManual.yaml")
                    # save_load_matrix.assert_affine_matrix_and_save(transform, transform_file_path)
                    #
                    # if calibration_result.valid():
                    #     messagebox.showinfo("Hand-Eye calibration OK", f"Result:\n{calibration_result}")
                    #     os.system(f"notepad.exe {transform_file_path}")
                    # else:
                    #     print("Hand-Eye calibration FAILED")
                    #     messagebox.showinfo('Error!', "Hand-Eye calibration FAILED")

        except Exception as exceptionmsg:
            messagebox.showerror('Error', f'{str(exceptionmsg)}')

    def warm_up_function(self):
        try:
            warmup.warmup(self.camera)
            messagebox.showinfo('Completed', "Camera Warm Up is completed!\n"
                                             "Your camera is ready for use.")

        except Exception as exceptionmsg:
            logging.error(str(exceptionmsg))
            messagebox.showerror('Error', 'Camera did not warm up!')

    def cam_intr(self):
        try:
            get_camera_intrinsics.camera_intr(self.camera)
            messagebox.showinfo('Completed', "Camera Intrinsics are ready!\n"
                                             "Check the files.")

        except Exception as exceptionmsg:
            logging.error(str(exceptionmsg))
            messagebox.showerror('Error', 'Could not get Intrinsics')


    def get_currJpose(self):
        try:
            if self.robot:
                if (self.JCoords.Entry1 or
                        self.JCoords.Entry2 or
                        self.JCoords.Entry3 or
                        self.JCoords.Entry4 or
                        self.JCoords.Entry5 or
                        self.JCoords.Entry6):
                    self.JCoords.Entry1.delete('1.0', 'end')
                    self.JCoords.Entry2.delete('1.0', 'end')
                    self.JCoords.Entry3.delete('1.0', 'end')
                    self.JCoords.Entry4.delete('1.0', 'end')
                    self.JCoords.Entry5.delete('1.0', 'end')
                    self.JCoords.Entry6.delete('1.0', 'end')

                vals = self.robot.get_curjpos()
                j1, j2, j3, j4, j5, j6 = vals[0], vals[2], vals[3], vals[4], vals[5], vals[6]
                self.JCoords.Entry1.insert('1.0', j1)
                self.JCoords.Entry2.insert('1.0', j2)
                self.JCoords.Entry3.insert('1.0', j3)
                self.JCoords.Entry4.insert('1.0', j4)
                self.JCoords.Entry5.insert('1.0', j5)
                self.JCoords.Entry6.insert('1.0', j6)

        except Exception as exceptionmsg:
            messagebox.showerror('Error!', f'{str(exceptionmsg)}')

    def start_calibration(self):
        if self.AutoCalib_button.get() == 1:
            self.automatic_calibration()
        elif self.ManualCalib_button.get() == 1:
            self.manual_calibration()

    def automatic_calibration(self):
        try:
            # Sending the robot to the desired position
            self.move_robot()

            matrix = functions_for_calibration.create_4x4_matrix(self.auto_calib_pose_dict[self.current_pose_id][0],
                                                                 self.auto_calib_pose_dict[self.current_pose_id][1],
                                                                 self.auto_calib_pose_dict[self.current_pose_id][2],
                                                                 self.auto_calib_pose_dict[self.current_pose_id][3],
                                                                 self.auto_calib_pose_dict[self.current_pose_id][4],
                                                                 self.auto_calib_pose_dict[self.current_pose_id][5])

            matrix_string = functions_for_calibration.matrix_to_string(matrix)

            elements = matrix_string.split(maxsplit=15)
            data = np.array(elements, dtype=np.float64).reshape((4, 4))
            robot_pose = zivid.calibration.Pose(data)
            print(f"The following pose was entered:\n{robot_pose}")

            with open("PosesAutomatic.txt", 'a') as file:
                file.write(f"Pose with index {self.current_pose_id}: {x}, {y}, {z}, {r}, {p}, {w}")

            frame = _assisted_capture(self.camera, self.current_pose_id)

            print("Detecting checkerboard in point cloud")
            detection_result = zivid.calibration.detect_feature_points(frame.point_cloud())

            if detection_result.valid():
                print("Calibration board detected")
                self.handeye_input.append(zivid.calibration.HandEyeInput(robot_pose, detection_result))
                self.current_pose_id += 1
            else:
                print(
                    "Failed to detect calibration board, ensure that the entire board is in the view of the camera"
                )

        except ValueError as ex:
            logging.error(f"{ex}")

        calibration_result = _perform_calibration(self.handeye_input, self.calibration_type)
        transform = calibration_result.transform()
        transform_file_path = Path(Path(__file__).parent / "CalibrationMatrixAutomated.yaml")
        save_load_matrix.assert_affine_matrix_and_save(transform, transform_file_path)

        if calibration_result.valid():
            messagebox.showinfo("Hand-Eye calibration OK", f"Result:\n{calibration_result}")
            os.system(f"notepad.exe {transform_file_path}")
        else:
            print("Hand-Eye calibration FAILED")
            messagebox.showinfo('Error!', "Hand-Eye calibration FAILED")

    def move_robot(self):
        try:
            current_pose_from_dict = self.auto_calib_pose_dict[self.current_pose_id]
            x = current_pose_from_dict[0]
            y = current_pose_from_dict[1]
            z = current_pose_from_dict[2]
            w = current_pose_from_dict[3]
            r = current_pose_from_dict[4]
            p = current_pose_from_dict[5]

        except Exception as exceptionmsg:
            messagebox.showerror("Error", "There is a problem with your poses!")

        try:
            self.robot.move(
                'joint',
                vals=[x, y, z, w, r, p],
                velocity=50,
                acceleration=70,
                cnt_val=0,
                # Maybe change to False
                linear=True
            )
        except Exception as ex:
            messagebox.showerror("Error", "There is a problem with moving your robot!")



    def manual_calibration(self):
        try:
            calibration_result = _perform_calibration(self.handeye_input, self.calibration_type)
            transform = calibration_result.transform()
            transform_file_path = Path(Path(__file__).parent / "CalibrationMatrixManual.yaml")
            save_load_matrix.assert_affine_matrix_and_save(transform, transform_file_path)

            if calibration_result.valid():
                messagebox.showinfo("Hand-Eye calibration OK", f"Result:\n{calibration_result}")
                os.system(f"notepad.exe {transform_file_path}")
            else:
                print("Hand-Eye calibration FAILED")
                messagebox.showinfo('Error!', "Hand-Eye calibration FAILED")

        except Exception as exceptionmsg:
            logging.error(f"{str(exceptionmsg)}")
            messagebox.showinfo('Error!', "Hand-Eye calibration FAILED")


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
        logging.basicConfig(filename="logging_file.log", level=logging.INFO)
        splash_screen = SplashScreen()
        splash_screen.after(3000, run_window)
        splash_screen.mainloop()

        app = App()
        app.mainloop()

    except Exception as ex:
        logging.error(f"Window exception: {ex}")
