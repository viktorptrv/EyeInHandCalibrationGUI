import threading
import tkinter as tk
import customtkinter as ctk
import zivid
import datetime
import yaml
import math
import numpy as np
import multiprocessing
from tkinter import messagebox
from CTkToolTip import *
from fanucpy import Robot
from PIL import Image, ImageTk
from warmup import warmup
from get_camera_intrinsics import camera_intrinsics
from pathlib import Path
from typing import List
from numpy import pi
from sample_utils.save_load_matrix import assert_affine_matrix_and_save

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

        self.image = Image.open("img.jpg")
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
        multiprocessing.Process(target=self.connect_to_cam_worker).start()

    def connect_to_cam_worker(self):
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
        multiprocessing.Process(target=self.init_robot_worker).start()

    def init_robot_worker(self):
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
        multiprocessing.Process(target=self.auto_calibration_worker).start()

    def auto_calibration_worker(self):

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

            return_value = self.calibrate_hand_eye(robot=self.robot_fanuc,
                                                   robot_joints=self.coordinates,
                                                   camera=self.camera)
            self.entry_pose.delete(0, 'end')
            self.entry_pose.insert(0, return_value)
        except Exception:
            messagebox.showinfo('Error!', 'You either pressed the button with no positions inserted '
                                          'or there was some kind of error!')

    def manual_calibration(self):
        multiprocessing.Process(target=self.manual_calibration_worker).start()

    def manual_calibration_worker(self):
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

            return_value = self.manual_calibrate_hand_eye(robot=self.robot_fanuc,
                                      camera=self.camera)

            self.entry_pose.delete(0, 'end')
            self.entry_pose.insert(0, return_value)

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
        if self.manual_calib_on:
            pass

    def matrix_to_string(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        matrix_string = ""

        for i in range(rows):
            for j in range(cols):
                matrix_string += str(matrix[i][j]) + " "

        return matrix_string.strip()

    def create_4x4_matrix(self, x1, y1, z1, r1, p1, w1):
        x, y, z, r, p, w = x1, y1, z1, r1, p1, w1
        a = r * pi / 180
        b = p * pi / 180
        c = w * pi / 180
        ca = math.cos(a)
        sa = math.sin(a)
        cb = math.cos(b)
        sb = math.sin(b)
        cc = math.cos(c)
        sc = math.sin(c)
        H = [[cb * cc, cc * sa * sb - ca * sc, sa * sc + ca * cc * sb, x],
            [cb * sc, ca * cc + sa * sb * sc, ca * sb * sc - cc * sa, y],
             [-sb, cb * sa, ca * cb, z],
             [0, 0, 0, 1]]
        return H

    def move_robot(self, robot_fanuc, joint_coordinates):
        x = joint_coordinates[0]
        y = joint_coordinates[1]
        z = joint_coordinates[2]
        a = joint_coordinates[3]
        b = joint_coordinates[4]
        c = joint_coordinates[5]

        try:
            robot_fanuc.move(
                'joint',
                vals=[x, y, z, a, b, c],
                velocity=50,
                acceleration=70,
                cnt_val=0,
                # Maybe change to False
                linear=True
            )
        except Exception as ex:
            print(str(ex))

    def _enter_robot_pose(self, robot_fanuc, index: int) -> zivid.calibration.Pose:
        """Robot pose user input.

        Args:
            index: Robot pose ID

        Returns:
            robot_pose: Robot pose

        """

        print(f"Current position: {robot_fanuc.get_curpos(robot_fanuc, 8, 8)}")
        current_pose = [float(i) for i in robot_fanuc.get_curpos(robot_fanuc, 8, 8)]
        x = current_pose[0]
        y = current_pose[1]
        z = current_pose[2]
        r = current_pose[3]
        p = current_pose[4]
        w = current_pose[5]

        with open("PosesAutomatic.txt",'a') as file:
            file.write(f"Pose with index {index}: {x}, {y}, {z}, {r}, {p}, {w}")

        matrix = self.create_4x4_matrix(x, y, z, r, p, w)

        # Saving the matrix as a YAML file
        # Later it can be used to verify the hand eye calibration with visualization
        with open(f"auto_pos{index}.yaml", 'w') as yaml_file:
            yaml.dump(matrix, yaml_file)

        print(f"Entering pose with id={index}")

        # inputted = input(
        #     f"Enter pose with id={index} (a line with 16 space separated values describing 4x4 row-major matrix):"
        # )

        # Converting the matrix to a one string and adding it as a pose
        inputted = self.matrix_to_string(matrix)

        # If the code above doesn't work, comment it out and uncomment the one below
        # flattened_matrix = [item for row in matrix for item in row]
        # inputted = ' '.join(map(str, flattened_matrix))

        elements = inputted.split(maxsplit=15)
        data = np.array(elements, dtype=np.float64).reshape((4, 4))
        robot_pose = zivid.calibration.Pose(data)
        print(f"The following pose was entered:\n{robot_pose}")
        return robot_pose

    def _perform_calibration(self, hand_eye_input: List[zivid.calibration.HandEyeInput]) -> zivid.calibration.HandEyeOutput:
        """Hand-Eye calibration type user input.

        Args:
            hand_eye_input: Hand-Eye calibration input

        Returns:
            hand_eye_output: Hand-Eye calibration result

        """
        while True:
            calibration_type = 'eih'
            # if calibration_type.lower() == "eth":
            #     print("Performing eye-to-hand calibration")
            #     hand_eye_output = zivid.calibration.calibrate_eye_to_hand(hand_eye_input)
            #     return hand_eye_output
            if calibration_type.lower() == "eih":
                print("Performing eye-in-hand calibration")
                hand_eye_output = zivid.calibration.calibrate_eye_in_hand(hand_eye_input)
                return hand_eye_output
            print(f"Unknown calibration type: '{calibration_type}'")

    def _assisted_capture(self, camera: zivid.Camera, current_pose) -> zivid.Frame:
        """
        Acquire frame with capture assistant.

        Args:
            camera: Zivid camera

        Returns:
            frame: Zivid frame

        """
        suggest_settings_parameters = zivid.capture_assistant.SuggestSettingsParameters(
            max_capture_time=datetime.timedelta(milliseconds=800),
            ambient_light_frequency=zivid.capture_assistant.SuggestSettingsParameters.AmbientLightFrequency.none,
        )
        settings = zivid.capture_assistant.suggest_settings(camera, suggest_settings_parameters)
        return_ply = camera.capture(settings)
        return_ply.save("img"+str(current_pose)+".zdf")
        return_ply.save('img'+str(current_pose)+'.png')
        return return_ply

    def calibrate_hand_eye(self, robot_joints, robot, camera):
        if not camera:
            app = zivid.Application()

            print("Connecting to camera")
            camera = app.connect_camera()
        output = ''
        current_pose_id = 0
        hand_eye_input = []
        calibrate = False

        if robot_joints:
            try:
                for i in range(len(robot_joints)):

                    try:
                        # Sending the robot to the desired position
                        self.move_robot(robot, robot_joints[current_pose_id])

                        robot_pose = self._enter_robot_pose(robot, current_pose_id)

                        frame = self._assisted_capture(camera, current_pose_id)

                        print("Detecting checkerboard in point cloud")
                        detection_result = zivid.calibration.detect_feature_points(frame.point_cloud())

                        if detection_result.valid():
                            print("Calibration board detected")
                            hand_eye_input.append(zivid.calibration.HandEyeInput(robot_pose, detection_result))
                            current_pose_id += 1
                        else:
                            print(
                                "Failed to detect calibration board, ensure that the entire board is in the view of the camera"
                            )
                    except ValueError as ex:
                        print(ex)

                calibration_result = self._perform_calibration(hand_eye_input)
                transform = calibration_result.transform()
                transform_file_path = Path(Path(__file__).parent / "CalibrationMatrixAutomated.yaml")
                assert_affine_matrix_and_save(transform, transform_file_path)

                if calibration_result.valid():
                    output = f"Hand-Eye calibration OK Result:\n{calibration_result}"

                else:
                    output = "Hand-Eye calibration FAILED"

                return output

            except Exception as ex:
                return ex
        else:
            var = 'No coordinates'
            return var

    def manual_calibrate_hand_eye(self, robot, camera):
        if not camera:
            app = zivid.Application()

            print("Connecting to camera")
            camera = app.connect_camera()

        current_pose_id = 0
        hand_eye_input = []
        calibrate = False

        while not calibrate:
            # command = input("Enter command, p (to add robot pose) or c (to perform calibration):").strip()
            while current_pose_id <= 20:
                try:
                    # Sending the robot to the desired position
                    input("Press Enter when ready to add the pose")
                    robot_pose = self._enter_robot_pose(robot, current_pose_id)

                    frame = self._assisted_capture(camera, current_pose_id)

                    print("Detecting checkerboard in point cloud")
                    detection_result = zivid.calibration.detect_feature_points(frame.point_cloud())

                    if detection_result.valid():
                        print("Calibration board detected")
                        hand_eye_input.append(zivid.calibration.HandEyeInput(robot_pose, detection_result))
                        current_pose_id += 1
                    else:
                        messagebox.showinfo('Not that bad of an Error', "Failed to detect calibration"
                                                                        " board, ensure that the entire board is "
                                                                        "in the view of the camera")
                        # print(
                        #     "Failed to detect calibration board, ensure that the entire board is in the view of the camera"
                        # )
                except ValueError as ex:
                    messagebox.showinfo('Error', f"The error is: {ex}")

            calibrate = True

        calibration_result = self._perform_calibration(hand_eye_input)
        transform = calibration_result.transform()
        transform_file_path = Path(Path(__file__).parent / "CalibrationMatrixManual.yaml")
        assert_affine_matrix_and_save(transform, transform_file_path)

        if calibration_result.valid():
            # print("Hand-Eye calibration OK")
            messagebox.showinfo("Hand-Eye calibration OK", f"Result:\n{calibration_result}")
            return calibration_result
        else:
            print("Hand-Eye calibration FAILED")
            messagebox.showinfo('Error!', "Hand-Eye calibration FAILED")


cur_pose = None
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

App()