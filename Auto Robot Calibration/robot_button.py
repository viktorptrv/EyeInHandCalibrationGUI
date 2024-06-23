from tkinter import messagebox
import customtkinter as ctk
from fanucpy import Robot


class RobotButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Connect Robot')
        self.configure(fg_color='#ffba33')
        self.configure(text_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)

    @staticmethod
    def connect_robot(q, ip, port_addr):
        try:
            is_robot_connected = None

            robot_fanuc = Robot(
                robot_model="LHMROB011",
                host=ip,
                port=port_addr,
                ee_DO_type="RDO",
                ee_DO_num=7)
            if not is_robot_connected:
                try:
                    robot_fanuc.connect()
                    is_robot_connected = True

                except Exception as ex:
                    print(ex)
                    is_robot_connected = False
                    messagebox.showinfo('Error!', 'You could not connect to the robot!\n'
                                                  'Check your network!')

                if is_robot_connected:
                    return q.append(is_robot_connected), q.append(robot_fanuc)

                return q.append(is_robot_connected)

        except Exception as ex:
            print(ex)

