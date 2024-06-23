import math
import numpy as np
from numpy import pi
import zivid
import datetime

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


def matrix_to_string(self, matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    matrix_string = ""

    for i in range(rows):
        for j in range(cols):
            matrix_string += str(matrix[i][j]) + " "

    return matrix_string.strip()


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


def perform_calibration(self, hand_eye_input: List[zivid.calibration.HandEyeInput], calibration_type) -> zivid.calibration.HandEyeOutput:
    """Hand-Eye calibration type user input.

    Args:
        hand_eye_input: Hand-Eye calibration input

    Returns:
        hand_eye_output: Hand-Eye calibration result

    """
    while True:
        # calibration_type = 'eih'

        if calibration_type.lower() == "eth":
            print("Performing eye-to-hand calibration")
            hand_eye_output = zivid.calibration.calibrate_eye_to_hand(hand_eye_input)
            return hand_eye_output
        if calibration_type.lower() == "eih":
            print("Performing eye-in-hand calibration")
            hand_eye_output = zivid.calibration.calibrate_eye_in_hand(hand_eye_input)
            return hand_eye_output
        print(f"Unknown calibration type: '{calibration_type}'")
