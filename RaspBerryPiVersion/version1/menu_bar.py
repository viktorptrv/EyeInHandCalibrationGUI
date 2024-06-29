from CTkMenuBar import *
import webbrowser


class MenuBar(CTkTitleMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.add_cascade('Robot Vision',
                         postcommand=lambda: webbrowser.open('https://www.wiredworkers.io/blog/robot-vision-how-does-it-work-and-what-can-you-do-with-it/'))
        self.add_cascade('Zivid',
                         postcommand=lambda: webbrowser.open('https://support.zivid.com/en/latest/index.html'))
        self.add_cascade('EiH Calibration',
                         postcommand=lambda: webbrowser.open('https://support.zivid.com/en/latest/academy/applications/hand-eye/hand-eye-calibration-problem.html'))


