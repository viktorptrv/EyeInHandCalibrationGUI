import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int

app = ctk.CTk(fg_color='#FF00FF')
app.geometry('300x200')
try:
    # Change the title bar color
    # get current window
    HWND = windll.user32.GetParent(app.winfo_id())
    title_bar_color = 0x000000FF
    title_bar_text_color = 0x0000FF99
    print(type(title_bar_color))
    windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        35,
                                        byref(c_int(title_bar_color)),
                                        sizeof(c_int))

    windll.dwmapi.DwmSetWindowAttribute(HWND,
                                        35,
                                        byref(c_int(title_bar_text_color)),
                                        sizeof(c_int))
except Exception as ex:
    print(ex)

app.mainloop()