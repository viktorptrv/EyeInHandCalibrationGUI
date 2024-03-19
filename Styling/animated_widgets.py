"""
You can create animated widgets in tkinter but you dont have prebuilt components
for it. You have to make your own.
To make your own, you need to use the after method and combine either with the layouts
or the configure method of the widget. Widgets can be updated in real time using either configure
or the layout methods. Calling a layout method multiple times on the same widget overrides the previous one
When animating widgets with layouts you want to use place. It is the only one that can change values pixel by pixel
the AFTER CONCEPT - after is a method of tkinter that can call a function after some time
window.after(amount of time, function)
A function called with after can call after itself
"""
import random
import customtkinter as ctk


def random_color():
    # Config
    colors = ['red', 'yellow', 'pink', 'green']
    num = random.randint(0, 3)
    color = colors[num]
    return print(color)


def move_btn():
    global button_x

    button_x += 0.001
    print(button_x)
    random_color()
    button.place(relx=button_x, rely=0.5, anchor='center')
    window.after(10, move_btn)


class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent, fg_color='red')
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)

        # animation logic
        self.pos = start_pos
        # if it is not in start position it will move towards start position
        self.in_start_pose = True

        self.place(relx=self.start_pos,
                   rely=0,
                   relwidth=self.width,
                   relheight=1)

    def animate(self):
        if self.in_start_pose:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        # move position to left until is reached end_pos
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx=self.pos,
                       rely=0,
                       relwidth=self.width,
                       relheight=1,)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pose = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx=self.pos,
                       rely=0,
                       relwidth=self.width,
                       relheight=1,)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pose = True


window = ctk.CTk()
window.geometry('600x400')
window.title('Animated Widgets')

# The left side of the frame is moved
# SlidePanel is simply a frame
animated_panel = SlidePanel(window, 0, -0.3)
ctk.CTkLabel(animated_panel, text = 'Label 1').pack(expand = True, fill = 'both', padx = 2, pady = 10)
ctk.CTkLabel(animated_panel, text = 'Label 2').pack(expand = True, fill = 'both', padx = 2, pady = 10)
ctk.CTkButton(animated_panel, text = 'Button', corner_radius = 0).pack(expand = True, fill = 'both', pady = 10)
ctk.CTkTextbox(animated_panel, fg_color = ('#dbdbdb','#2b2b2b')).pack(expand = True, fill = 'both', pady = 10)

button_x = 0.5
button = ctk.CTkButton(master=window,
                       text='toggle sidebar',
                       command=animated_panel.animate)
button.place(relx=button_x, rely=0.5, anchor='center')

window.mainloop()