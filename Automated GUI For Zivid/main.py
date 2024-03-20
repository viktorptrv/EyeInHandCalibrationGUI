from warmup import warmup
from get_camera_intrinsics import _main
from hand_in_eye_calibration import calibrate_hand_eye
from manual_hand_eye_calibration import manual_calibrate_hand_eye
# from convert_intrinsics_opencv_to_halcon import _main
import zivid
from fanucpy import Robot


# За да не пипаме сорс кода на библиотеката fanucpy
# си създаваме функция, която наподобява функцията get_curpos
# С новосъздадената функция заменяме get_curpos чрез метода "monkey patching)
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


# Initializing the robot
robot_fanuc = Robot(
    robot_model="LHMROB011",
    host="10.37.115.206",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
)

robot_fanuc.connect()

# Заменяне на метода:
robot_fanuc.get_curpos = get_curposv2
# Когато искаме да използваме новия метод е нужно като аргумент да вкарваме
# и създаденият обект от клас Robot:
# robot_fanuc.get_curpos(robot_fanuc, 8, 8)

if input("Camera warm up? -y/n: ").lower() == 'y':
    warmup()

if input("Camera intrinsics? -y/n: ").lower() == 'y':
    _main()
    # if input("Camera intrinsics to halcon? -y/n").lower() == 'y':

if input("Camera calibration? -y/n: ").lower() == 'y':

    """
    This is an example with 4 joint poses of the robot
    Use 10 to 20 joint coordinates of the robot. Add them to the dictionary
    """

    robot_joint_dict = {
        0: [-63.661, 11.028, -18.779, -8.969, -71.210, 63.251],
        1: [-61.828, 7.715, -19.530, -9.013, -70.198, 61.563],
        2: [-69.737, 5.638, -18.798, -15.513, -70.272, 71.780],
        3: [-60.138, 24.443, -15.028, -6.313, -87.852, 57.871],
        4: [-57.360, 19.090, -17.595, -6.946, -84.992, 55.515],
        5: [-52.418, 11.337, -19.787, -3.331, -75.853, 50.116],
        6: [-47.526, 5.556, -22.036, 1.228, -68.008, 43.736],
        7: [-41.769, 0.164, -23.593, 4.738, -63.864, 36.414],
        8: [-34.501, -5.233, -24.422, 7.934, -62.046, 27.608],
        9: [-41.479, 10.815, -21.020, 3.571, -75.484, 36.983],
        10: [-38.665, 13.360, -21.334, 5.363, -78.056, 33.668],
        11: [-41.749, 16.371, -20.393, 5.852, -78.715, 36.690],
        12: [-36.406, 12.072, -24.192, 4.974, -75.441, 30.948],
        13: [-24.338, -8.382, -26.716, 11.870, -60.661, 15.329],
        14: [-56.740, 22.812, -22.462, -4.040, -76.165, 54.834],
        15: [-47.282, 29.212, -18.060, 4.027, -89.430, 42.548],
        16: [-31.919, 13.118, -26.493, 7.377, -76.577, 24.061],
        17: [-64.056, 0.28, -21.950, -15.066, -65.339, 66.549],
        18: [-71.9, 14.171, -25.511, -19.982, -69.696, 81.561],
        19: [-66.442, 12.985, -22.366, -11.465, -74.791, 93.734],
        20: [-66.359, 16.622, -21.983, -11.080, -81.626, 92.365],
        21: [-39.434, 3.078, -23.571, 3.357, -67.563, 40.355],
        22: [-36.730, 13.428, -21.944, 5.194, -80.238, 34.712],
        23: [-35.831, 17.163, -30.553, 6.765, -74.048, 32.469],
        24: [-58.884, 16.059, -22.693, -5.470, -70.990, 61.809],
        # 25: [-60.144, 21.081, -26.716, -7.449, -72.147, 58.927],
        25: [-34.801, -8.675, -24.801, 4.586, -60.165, 28.894],
        26: [-42.210, 0.737, -36.378, 4.414, -48.125, 35.620],
        27: [-59.955, 7.332, -24.389, -9.136, -65.681, 58.289],
        28: [-61.288, 13.643, -34.176, -10.028, -56.221, 61.462]
    }
    if input("Automatic (Type a) or Manual calibration (Type b)?\n ").lower() == 'b':
        manual_calibrate_hand_eye(robot_fanuc)
    else:
        calibrate_hand_eye(robot_joint_dict, robot_fanuc)


