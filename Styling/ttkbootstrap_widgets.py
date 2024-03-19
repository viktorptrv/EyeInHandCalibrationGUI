import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.widgets import DateEntry, Floodgauge, Meter

window = ttk.Window(themename='journal')
window.geometry('400x400')
window.title('Extra Widgets')

# Scrollable frame
# scrolled_frame = ScrolledFrame(master=window)
# scrolled_frame.pack(expand=True, fill='both')

# for i in range(100):
#     frame = ttk.Frame(scrolled_frame)
#     ttk.Label(master=frame,
#               text=f'Label: {i}').pack()
#     ttk.Button(master=frame,
#                text=f'ButtonL {i}').pack()
#     frame.pack()

# Toast is a notification message
toast = ToastNotification(title='This is a message title',
                          message='Actual message',
                          duration=2000,
                          alert=True)

ttk.Button(window,
           text='show toast',
           command=toast.show_toast).pack()

# Tooltip - gives tips on the buttons
button = ttk.Button(master=window,
                    text='tooltip button',
                    bootstyle='warning')
button.pack()

ToolTip(button, text='This does something')

# Calendar
calendar = DateEntry(master=window)
calendar.pack()

ttk.Button(master=window,
           text='Get calendar date',
           command=lambda: print(calendar.entry.get())).pack()

# Progress bar -> floodgauge
progress_int = ttk.IntVar(value=50)
progress = ttk.Floodgauge(window,
                          text='progress',
                          variable=progress_int,
                          mask='mask {}')
progress.pack(pady=10, fill='x')

ttk.Scale(window,
          from_=0,
          to=100,
          variable=progress_int).pack()

# Meter
ttk.Meter(master=window).pack()

window.mainloop()