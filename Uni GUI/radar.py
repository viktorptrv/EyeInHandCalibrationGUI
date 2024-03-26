import tkinter as tk

import customtkinter
import customtkinter as ctk


def run_program():
    pass


def stop_program():
    pass


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

window = ctk.CTk()
window.geometry('900x600')
window.title('Radar with LabView and Arduino')
window.maxsize(900,600)
window.minsize(900,600)

window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.columnconfigure(index=3, weight=1)

window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)

menu = tk.Menu(master=window)
window.config(menu=menu)

menu_buttons = ctk.CTkFrame(master=window)
menu_buttons.grid(column=0, row=0, rowspan=3, sticky='nswe', pady=10, padx=10)

menu_buttons.columnconfigure(index=0, weight=1)
menu_buttons.columnconfigure(index=1, weight=1)

menu_buttons.rowconfigure(index=0, weight=1)
menu_buttons.rowconfigure(index=1, weight=1)
menu_buttons.rowconfigure(index=2, weight=1)

menu_radar = ctk.CTkFrame(master=window)
menu_radar.grid(column=1, row=0, rowspan=3, columnspan=3, sticky='nswe', pady=10, padx=10)

# file_menu = tk.Menu(master=menu,
#                     tearoff=False) # tearoff removes '----'
#
# menu.add_cascade(label='Documentation', menu=file_menu)
#
# file_menu.add_command(label='Open Documentation',
#                       command=lambda: print('New file'))
# file_menu.add_separator()

scale_int = tk.IntVar(value=10)
speed_slider = ctk.CTkSlider(master=menu_buttons,
                             command=lambda value: print(scale_int.get()),
                             from_=0,
                             to=100,
                             variable=scale_int,
                             orientation='vertical',
                             width=30)
speed_slider.grid(row=1, column=0)

angle_int = tk.IntVar(value=10)
angle_slider = ctk.CTkSlider(master=menu_buttons,
                             command=lambda value: print(scale_int.get()),
                             from_=0,
                             to=100,
                             orientation='vertical',
                             variable=angle_int,
                             width=30)
angle_slider.grid(row=1, column=1)

start_button = ctk.CTkButton(master=menu_buttons,
                             text='Start',
                             command=run_program)

start_button.grid(row=0, column=0, columnspan=2)

stop_button = ctk.CTkButton(master=menu_buttons,
                            text='Stop',
                            command=stop_program)
stop_button.grid(row=2, column=0, columnspan=2)

window.mainloop()
