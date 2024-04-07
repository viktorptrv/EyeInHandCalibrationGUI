"""
Perform a touch test with a robot to verify Hand-Eye Calibration using the RoboDK interface.

The touch test is performed by a robot equipped with the Pointed Hand-Eye Verification Tool.
The robot touches a corner of the checkerboard on the Zivid calibration board to verify hand-eye calibration.
The sample requires as follows:
- Type of calibration used (eye-in-hand or eye-to-hand)
- YAML file with Hand-Eye transformation
- YAML file with Pointed Hand-Eye Verification Tool transformation
- Capture pose target name used in RoboDK

Note: Make sure to launch your RDK file and connect to the robot through RoboDK before running this script.

You can find the complete tutorial with a detailed explanation at: https://support.zivid.com/en/latest/academy/applications/hand-eye/hand-eye-calibration-verification-via-touch-test.html

More information about RoboDK is available at: https://robodk.com/doc/en/Getting-Started.html

"""

import argparse
import datetime

import numpy as np
import math
import zivid
from fanucpy import Robot
from numpy import pi
# from sample_utils.robodk_tools import connect_to_robot, get_robot_targets, set_robot_speed_and_acceleration
from sample_utils.save_load_matrix import load_and_assert_affine_matrix


def matrix_to_position(m):
    x = m[0][3]
    y = m[1][3]
    z = m[2][3]

    roll = math.atan2(m[2][1], m[2][2]) * 180 / math.pi
    pitch = math.atan2(-m[2][0], math.sqrt(m[2][1] ** 2 + m[2][2] ** 2)) * 180 / math.pi
    yaw = math.atan2(m[1][0], m[0][0]) * 180 / math.pi
    pose = [x, y, z, roll, pitch, yaw]
    return pose


def create_4x4_matrix(x1, y1, z1, r1, p1, w1):
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


def get_curposv2(self, uframe, tframe) -> list[float]:
    """Gets current cartesian position of tool center point.

    Returns:
        list[float]: Current positions XYZWPR.
    """

    cmd = f"curpos:{9}:{1}"
    print(cmd)
    _, msg = self.send_cmd(cmd)
    print(f"msg: {msg}")
    vals = [float(val.split("=")[1]) for val in msg.split(",")]
    print(f"Vals: {vals}")
    return vals


def _capture_and_estimate_calibration_board_pose(camera: zivid.Camera) -> np.ndarray:
    """Capture an image with the Zivid camera using capture assistant, detecting, and estimating the pose of the calibration board.

    Args:
        camera: Zivid camera

    Returns:
        calibration_board_pose: A 4x4 numpy array containing the calibration board pose

    """
    suggest_settings_parameters = zivid.capture_assistant.SuggestSettingsParameters(
        max_capture_time=datetime.timedelta(milliseconds=800),
        ambient_light_frequency=zivid.capture_assistant.SuggestSettingsParameters.AmbientLightFrequency.none,
    )

    settings_list = zivid.capture_assistant.suggest_settings(camera, suggest_settings_parameters)
    frame = camera.capture(settings_list)

    calibration_board_pose = zivid.calibration.detect_feature_points(frame.point_cloud()).pose().to_matrix()

    return calibration_board_pose


def _get_robot_base_to_calibration_board_transform(
    user_options: argparse.Namespace,
    camera_to_calibration_board_transform: np.ndarray,
    robot,
) -> np.ndarray:
    """Calculating the robot base to the calibration board transform matrix.

    Args:
        user_options: Arguments from user that contain the type of hand-eye calibration done and the path to the matrix that resulted from that calibration
        camera_to_calibration_board_transform: A 4x4 numpy array containing the calibration board pose in the camera frame
        robot: Robot item in open RoboDK rdk file

    Returns:
        robot_base_to_calibration_board_transform: A 4x4 numpy array containing the calibration board pose in the robot base frame

    """
    if user_options.eih:
        print("Loading current robot pose")
        # robot_base_to_flange_transform = np.array(robot.get_curpos(robot, 8, 8)).T

        current_pose_of_robot = robot.get_curpos(robot, 8, 8)
        print("Current pose of the robot: ", current_pose_of_robot)
        input()
        x = current_pose_of_robot[0]
        y = current_pose_of_robot[1]
        z = current_pose_of_robot[2]
        r = current_pose_of_robot[3]
        p = current_pose_of_robot[4]
        w = current_pose_of_robot[5]
        matrix = create_4x4_matrix(x, y, z, r, p, w)

        robot_base_to_flange_transform = np.array(matrix)

        flange_to_camera_transform = load_and_assert_affine_matrix(user_options.hand_eye_yaml)
        print("Robot base to flange: ", robot_base_to_flange_transform)
        print("flange to camera: ", flange_to_camera_transform)
        print("Camera to calibration board: ", camera_to_calibration_board_transform)
        input()
        robot_base_to_calibration_board_transform = (
            robot_base_to_flange_transform @ flange_to_camera_transform @ camera_to_calibration_board_transform
        )
        print("Robot Base to calibration board transformation: ", robot_base_to_calibration_board_transform)

    return robot_base_to_calibration_board_transform


def _yes_no_prompt(question: str) -> str:
    """Gets a yes or no answer to a given question.

    Args:
        question: A question what requires a yes or no answer

    Returns:
        String containing 'y' or 'n'

    """
    while True:
        response = input(f"{question} (y/n): ")
        if response in ["n", "N", "y", "Y"]:
            return response.lower()
        print("Invalid response. Please respond with either 'y' or 'n'.")


def _options() -> argparse.Namespace:
    """Function to read user arguments.

    Returns:
        Arguments from user

    """

    parser = argparse.ArgumentParser(description=__doc__)

    type_group = parser.add_mutually_exclusive_group(required=True)
    type_group.add_argument("--eih", "--eye-in-hand", action="store_true", help="eye-in-hand calibration")
    # type_group.add_argument("--eth", "--eye-to-hand", action="store_true", help="eye-to-hand calibration")

    parser.add_argument("--ip", required=False, help="10.37.115.206")
    parser.add_argument(
        "--target-keyword",
        required=True,
        help="touch_test_pose.yaml",
    )
    parser.add_argument(
        "--tool-yaml",
        required=True,
        help="pointed-hand-eye-verification-tool.yaml",
    )
    parser.add_argument(
        "--mounts-yaml",
        required=False,
        help="on-arm-mounts.yaml",
    )
    parser.add_argument(
        "--hand-eye-yaml",
        required=True,
        help="transform.yaml",
    )

    return parser.parse_args()

# Input into the terminal:
# python touch_test.py --eih --target-keyword touch_test_pose.yaml --tool-yaml pointed-hand-eye-verification-tool.yaml --mounts-yaml on-arm-mounts.yaml --hand-eye-yaml transform.yaml


def zivid_robot_touch_test(robot) -> None:
    user_options = _options()
    app = zivid.Application()
    print("connecting to camera next")
    camera = app.connect_camera()
    print("Camera connected")

    print("Loading the Pointed Hand-Eye Verification Tool transformation matrix from a YAML file")
    pointed_hand_eye_verification_tool_matrix = load_and_assert_affine_matrix(user_options.tool_yaml)

    if user_options.mounts_yaml:
        print("Loading the on-arm mounts transformation matrix from a YAML file")
        flange_to_on_arm_mounts_transform = load_and_assert_affine_matrix(user_options.mounts_yaml)

        tcp = flange_to_on_arm_mounts_transform @ pointed_hand_eye_verification_tool_matrix
    else:
        tcp = pointed_hand_eye_verification_tool_matrix

    capture_pose = [
        [0.9969105930695031, -0.07005982715024156, 0.035509013580918715, 224.994],
        [-0.0734009656756829, -0.9918971373003053, 0.10369362204753228, -547.098],
        [0.02795653168203835, -0.10597966613996067, -0.9939752223778888, 86.314],
        [0, 0, 0, 1]]

    if not capture_pose:
        raise IndexError(
            "The list of poses retrieved from RoboDK is empty...\nMake sure that you have created a Capture Pose and that you introduced the right keyword for it."
        )

    capture_pose_non_matrix = [77.28, -308.72, 319.00, -8.03, -16.50, -85.60]
    x = capture_pose_non_matrix[0]
    y = capture_pose_non_matrix[1]
    z = capture_pose_non_matrix[2]
    r = capture_pose_non_matrix[3]
    p = capture_pose_non_matrix[4]
    w = capture_pose_non_matrix[5]

    try:
        robot.move(
            'joint',
            vals=[x, y, z, r, p, w],
            velocity=50,
            acceleration=70,
            cnt_val=0,
            # Maybe change to False
            linear=True
        )
    except Exception as ex:
        print(str(ex))

    print("\nPlace the calibration board in the FOV of the camera.")
    input("Press enter to start.")

    while True:
        try:
            print("Detecting the calibration board pose (upper left checkerboard corner)")
            camera_to_calibration_board_transform = _capture_and_estimate_calibration_board_pose(camera)

            print("Calculating the calibration board pose in robot base frame")
            robot_base_to_calibration_board_transform = _get_robot_base_to_calibration_board_transform(
                user_options,
                camera_to_calibration_board_transform,
                robot
            )

            print("Calculating pose for robot to touch the calibration board")
            touch_pose = robot_base_to_calibration_board_transform @ np.linalg.inv(tcp)

            print("Calculating pose for the robot to approach the calibration board")
            touch_pose_offset = np.identity(4)
            touch_pose_offset[1, 2] = -10

            # '@' is used for matrix multiplication when used with objects that support the '__matmul__()' method
            approach_pose = touch_pose @ touch_pose_offset

            print("Approach pose: ", approach_pose)
            print("Touch Pose: ", touch_pose)

            approach_pose = matrix_to_position(approach_pose)
            touch_pose = matrix_to_position(touch_pose)

            print("Touching calibration board (upper left checkerboard corner)")

            x = approach_pose[0]
            y = approach_pose[1]
            z = approach_pose[2]
            a = approach_pose[3]
            b = approach_pose[4]
            c = approach_pose[5]

            print("x,y,z,a,b,c: ", x, y, z, a, b, c)

            x1 = touch_pose[0]
            y1 = touch_pose[1]
            z1 = touch_pose[2]
            a1 = touch_pose[3]
            b1 = touch_pose[4]
            c1 = touch_pose[5]

            print("x1,y1,z1,a1,b1,c1: ", x1, y1, z1, a1, b1, c1)

            robot.move('pose',
                vals=[x, y, z, a, b, c],
                velocity=30,
                acceleration=70,
                cnt_val=0,
                # Maybe change to False
                linear=False)

            robot.move('pose',
                vals=[x1, y1, z1, a1, b1, c1],
                velocity=50,
                acceleration=70,
                cnt_val=0,
                # Maybe change to False
                linear=False)

            input("\nPress enter to pull back and return to the capture pose...")
            # robot.MoveL(Mat(approach_pose.tolist()))
            robot.move('pose',
                       vals=[x, y, z, a, b, c],
                       velocity=50,
                       acceleration=70,
                       cnt_val=0,
                       # Maybe change to False
                       linear=True)
            # robot.MoveJ(capture_pose[0])

            print("\nThe board can be moved at this time.")
            answer = _yes_no_prompt("Perform another touch?")
            if answer == "n":
                break

        except RuntimeError as ex:
            print(ex)
            print("Please make sure calibration board is in FOV.")
            input("Press enter to continue.")


robot_fanuc = Robot(
    robot_model="LHMROB011",
    host="10.37.115.206",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
)

robot_fanuc.connect()

robot_fanuc.get_curpos = get_curposv2

zivid_robot_touch_test(robot_fanuc)