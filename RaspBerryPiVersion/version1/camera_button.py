import logging
import queue
import time
import zivid

import customtkinter as ctk
from tkinter import messagebox


class CameraButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Connect Camera')
        self.configure(fg_color='#ffba33')
        self.configure(text_color='black')
        self.configure(anchor='center')
        self.configure(width=200)
        self.configure(height=40)
        # self.configure(command=self.remove_image)

    @staticmethod
    def connect_camera(q):
        app = None

        is_camera_connected = False

        try:
            app = zivid.Application()
            app.connect_camera()
            is_camera_connected = True

        except Exception as ex:
            messagebox.showinfo('Error', 'You could not connect to the camera!\n'
                                         'Check your network!')
            logging.error(f"Camera Exception: {ex}")

        if app:
            return q.append(is_camera_connected), q.append(app)


