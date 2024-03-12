"""
Canvas is a widget that allows you to 'draw' shapes

"""
import tkinter as tk

window = tk.Tk()
window.geometry('500x800')
window.title('Canvas')

# Creating a canvas
# bg- background to make the widget visable
canvas = tk.Canvas(master=window,
                   bg='white')
canvas.pack()

# Different methods of a canvas object
canvas.create_rectangle((0, 0, 100, 200))

window.mainloop()