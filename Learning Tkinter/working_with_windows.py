"""
We can change a windows opacity, position,
full screen, title bar
"""
import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title('More on the window')
# window.geometry('600x400+left_pose+top_pose')
window.geometry('600x400+0+0')

# Change icon use ICO file!!!
window.iconbitmap("C:/Users/vikos/Downloads/Teacher's Copy.ico")

# Window sizes
window.minsize(width=200, height=300)
window.maxsize(width=600, height=400)

window.resizable(True, False)   # scale only horizontally and not vertically

# Screen attributes
print(window.winfo_screenwidth())
print(window.winfo_screenheight())

# Window attributes
window.attributes('-alpha', 0.3)  # 1- transparancy, 0 - invinsible
window.attributes('-topmost', True)

# Security event
window.bind('<Escape>', lambda event: window.quit())
# window.attributes('-disable', True)  # Disabling the window
# window.attributes('-fullscreen', True)  # Start at full screen

# Title bar
window.overrideredirect(True)   # Cant see the title bar to close the app or resize the map

window.mainloop()