import math
from numpy import pi

def matrix_to_position(H):
    x = H[0][3]
    y = H[1][3]
    z = H[2][3]

    roll = math.atan2(H[2][1], H[2][2]) * 180 / math.pi
    pitch = math.atan2(-H[2][0], math.sqrt(H[2][1] ** 2 + H[2][2] ** 2)) * 180 / math.pi
    yaw = math.atan2(H[1][0], H[0][0]) * 180 / math.pi

    return x, y, z, roll, pitch, yaw


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


capture_pose_non_matrix = [224.994, -547.098, 86.314, -173.914, -1.602, -4.211]
x = capture_pose_non_matrix[0]
y = capture_pose_non_matrix[1]
z = capture_pose_non_matrix[2]
r = capture_pose_non_matrix[3]
p = capture_pose_non_matrix[4]
w = capture_pose_non_matrix[5]

matrix = create_4x4_matrix(x,y,z,r,p,w)
x, y, z, roll, pitch, yaw = matrix_to_position(matrix)
print("Position:")
print("x:", x)
print("y:", y)
print("z:", z)
print("Orientation (roll, pitch, yaw):")
print("roll:", roll)
print("pitch:", pitch)
print("yaw:", yaw)


