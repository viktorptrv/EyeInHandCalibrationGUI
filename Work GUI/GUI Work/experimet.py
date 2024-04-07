import time
import tkinter as tk
import multiprocessing
import customtkinter as ctk
from PIL import Image, ImageTk


def connect_cam():
    button_cam.pack_forget()
    button_cam.pack(padx=10, pady=10)
    img1 = ctk.CTkImage(Image.open('camera.png'))
    button_cam.configure(image=img1)


ctk.set_appearance_mode('dark')

window = ctk.CTk()
window.geometry('1100x500')
window.title('Experiment')

window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.columnconfigure(index=3, weight=1)
window.columnconfigure(index=4, weight=1)
window.columnconfigure(index=5, weight=1)


window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)
window.rowconfigure(index=3, weight=1)
window.rowconfigure(index=4, weight=1)
window.rowconfigure(index=5, weight=1)

frame_one = ctk.CTkFrame(master=window, fg_color='#0AFFB5')
frame_one.grid(column=0, row=0, columnspan=3, rowspan=6,  sticky='nswe')

frame_two = ctk.CTkFrame(master=window)
frame_two.grid(column=3, row=0, columnspan=3, rowspan=6,  sticky='nswe')

button_cam = ctk.CTkButton(master=frame_one,
                           text='Connect Camera',
                           fg_color='white',
                           text_color='black',
                           command=connect_cam)
button_cam.pack(padx=10, pady=10)

window.mainloop()
