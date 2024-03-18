"""
In terms of styling, customtkinter is the best
Customtkinter uses the same widgets as ttk but lets you customise them easily
It also has additional widgets and each widget has a a dark and light mode
"""
import tkinter

import customtkinter as ctk

window = ctk.CTk()
window.title('customtkinter app')
window.geometry('600x600')

ctk.set_appearance_mode("dark")

# Widgets
string_var = tkinter.StringVar(value='custom label')
label = ctk.CTkLabel(master=window,
                     text='Ctk label',
                     fg_color='red',
                     text_color='blue',
                     corner_radius=10,
                     text_variable=string_var)
label.pack()

button = ctk.CTkButton(master=window,
                       text='A button',
                       fg_color='blue',
                       text_color='white',
                       corner_radius=10,
                       hover_color='#AA0',
                       command=lambda: ctk.set_appearance_mode('light'))
button.pack()

frame = ctk.CTkFrame(master=window)
frame.pack()

window.mainloop()