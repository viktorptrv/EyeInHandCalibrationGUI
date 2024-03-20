from fanucpy import Robot
import yaml
from numpy import pi
import math


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
current_pose = [float(i) for i in robot_fanuc.get_curpos(robot_fanuc, 8, 8)]

print(current_pose)
x = current_pose[0]
y = current_pose[1]
z = current_pose[2]
r = current_pose[3]
p = current_pose[4]
w = current_pose[5]

matrix = create_4x4_matrix(x, y, z, r, p, w)

matrix_str = '[\n'
for row in matrix:
    matrix_str += '    ' + '[' + ', '.join(map(str, row)) + '],\n'
matrix_str += ']'

print(matrix_str)

with open("../../../../Downloads/Python Calibration of Zivid/Python Calibration of Zivid/capture_touch_test_pose.yaml", 'w') as file:
    yaml.dump(matrix_str, file)
