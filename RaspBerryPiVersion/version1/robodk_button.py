from robodk.robolink import *
import customtkinter as ctk


class RobodkButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='RoboDk Calibration Simulation')
        self.configure(fg_color='#ffba33')
        self.configure(text_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)

    @staticmethod
    def simulation(targets_dict):
        targets = [value for key, value in targets_dict.items()]

        RDK = Robolink()  # establish a link with the simulator
        # active_station = RDK.setActiveStation("C:/Users/vikos/Desktop/Дипломна Работа Бакалавър/Fanuc_Zivid_Station.rdk")
        # Turn off rendering (faster)
        RDK.Render(False)
        prog = RDK.AddProgram('AutoProgram')

        # Hide program instructions (optional, but faster)
        prog.ShowInstructions(False)

        robot = RDK.Item('Fanuc CRX-10iA/L')  # retrieve the robot by name
        tcp = RDK.Item('Zivid Pointed Hand-Eye Verification Tool')
        robot.setSpeed(speed_linear=10)
        robot.setVisible(visible=True, visible_frame=False)
        robot.setJoints([0, 0, 0, 0, 0, 0])  # set all robot axes to zero

        current_target = -1

        pose_ref = robot.Pose()  # Retrieve the current robot position

        while current_target <= len(targets) - 1:
            # Create a new target
            target = RDK.AddTarget(name=f"Target {current_target}",
                                   itemparent=tcp,
                                   itemrobot=robot,
                                   )

            # Use the reference pose and update the XYZ Position
            pose_ref.setPos(targets[current_target])
            target.setPose(pose_ref)

            target.setAsCartesianTarget()

            prog.MoveL(target=target)

            current_target += 1

            robot.MoveJ(target=target)

        # Hide the target items from the tree: it each movement still keeps its own target.
        # Right click the movement instruction and select "Select Target" to see the target in the tree
        prog.ShowTargets(False)

        # Turn rendering ON before starting the simulation (automatic if we are done)
        RDK.Render(True)

        # --------------------------------------
        # Update the program path to display the yellow path in RoboDK.
        # Set collision checking ON or OFF
        check_collisions = COLLISION_OFF
