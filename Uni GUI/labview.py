import math
import random


def is_it_in_the_limit(i, x, y):
    value = False

    iterations_floored = i - (360 * math.floor(i/360))

    atan_xy = math.atan2(x, y)
    atan_pi = (atan_xy / (2 * math.pi)) * 360
    floored = atan_pi - (360 * math.floor(atan_pi/360))

    upper_limit = floored + 0.5
    lower_limit = floored - 0.5

    if upper_limit > iterations_floored > lower_limit:
        value = True

    return value

