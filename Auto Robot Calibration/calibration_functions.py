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
# from warmup import warmup
# from get_camera_intrinsics import camera_intrinsics
from pathlib import Path
from typing import List
from numpy import pi


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

    with open("PosesAutomatic.txt", 'a') as file:
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
    return_ply.save("img" + str(current_pose) + ".zdf")
    return_ply.save('img' + str(current_pose) + '.png')
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