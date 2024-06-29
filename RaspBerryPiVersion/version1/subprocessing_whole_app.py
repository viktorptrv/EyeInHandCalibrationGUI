import multiprocessing
import subprocess
import threading
from tkinter import messagebox

from main import app


def check_robot_connection():
    print('thread r start')
    while True:
        if not app.camera:
            messagebox.showwarning("Error!", "Camera is not connected again")


def check_camera_connection():
    print('thread c start')
    while True:
        if not app.robot:
            messagebox.showwarning("Error!", "Robot is not connected")


def is_calibration_ready():
    print('thread cc start')
    while True:
        if app.camera and app.robot:
            if app.calibration_type == 'eih' and app.auto_calib_pose_dict:
                app.CalibrateButton.configure(state="normal")
                app.CalibrateButton.configure(fg_color='#2DFE54')
                app.CalibrateButton.configure(command=app.calibrate_eye_in_hand)
            elif app.calibration_type == 'eth':
                app.CalibrateButton.configure(state="normal")
                app.CalibrateButton.configure(fg_color='#2DFE54')
                app.CalibrateButton.configure(command=app.calibrate_eye_to_hand)


if __name__ == '__main__':
    thread_robot_connection = multiprocessing.Process(target=check_robot_connection,
                                                      daemon=True)
    thread_camera_connection = multiprocessing.Process(target=check_camera_connection,
                                                       daemon=True)
    thread_ready_calibration = multiprocessing.Process(target=is_calibration_ready)

    thread_camera_connection.start()

    thread_robot_connection.start()
    thread_ready_calibration.start()
