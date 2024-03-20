from importlib import util
import sys
from fanucpy import Robot


def modify_and_import(module_name, package, modification_func):
    spec = util.find_spec(module_name, package)
    source = spec.loader.get_source(module_name)
    new_source = modification_func(source)
    module = util.module_from_spec(spec)
    codeobj = compile(new_source, module.__spec__.origin, 'exec')
    exec(codeobj, module.__dict__)
    sys.modules[module_name] = module
    return module


# Initializing the robot
robot_fanuc = Robot(
    robot_model="LHMROB011",
    host="10.37.115.206",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
)

robot_fanuc.connect()

modify_and_import(robot_fanuc.get_curpos(), fanucpy, )