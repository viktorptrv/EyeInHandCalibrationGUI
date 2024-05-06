import tkinter as tk
import customtkinter as ctk

from PIL import Image, ImageTk


class ImageRobot(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/robotic-arm.png'),
                                          dark_image=Image.open('Images/robotic-arm.png'),
                                          size=(80, 80)))
        self.configure(text='')


class ImageCam(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/camera.png'),
                                          dark_image=Image.open('Images/camera.png'),
                                          size=(100, 100)))
        self.configure(text='')


class ImageIntr(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image_intr_button_blur.webp'),
                                          dark_image=Image.open('Images/image_intr_button_blur.webp'),
                                          size=(200, 40)))
        self.configure(text='')


class CamButtonBlur(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image_cam_button_blur.webp'),
                                          dark_image=Image.open('Images/image_cam_button_blur.webp'),
                                          size=(200, 40)))
        self.configure(text='')


class WarmUpBlur(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image-6.webp'),
                                          dark_image=Image.open('Images/image-6.webp'),
                                          size=(200, 40)))
        self.configure(text='')


class CurrPoseBlur(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image-8.webp'),
                                          dark_image=Image.open('Images/image-8.webp'),
                                          size=(200, 40)))
        self.configure(text='')


class CurrJPoseBlur(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image-9.webp'),
                                          dark_image=Image.open('Images/image-9.webp'),
                                          size=(200, 40)))
        self.configure(text='')


class SendRobotBlur(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(image=ctk.CTkImage(light_image=Image.open('Images/image-11.webp'),
                                          dark_image=Image.open('Images/image-11.webp'),
                                          size=(200, 40)))
        self.configure(text='')
