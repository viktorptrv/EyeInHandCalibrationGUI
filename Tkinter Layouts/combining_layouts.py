import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('600x600')
window.minsize(600, 600)

# Main layout widgets
menu_frame = ttk.Frame(master=window)
main_frame = ttk.Frame(master=window)

menu_frame.place(x=0, y=0, relwidth=0.3, relheight=1)

main_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

# menu widgets
menu_button1 = ttk.Button(master=menu_frame, text='Button 1')
menu_button2 = ttk.Button(master=menu_frame, text='Button 2')
menu_button3 = ttk.Button(master=menu_frame, text='Button 3')

menu_slider1 = ttk.Scale(master=menu_frame, orient='vertical')
menu_slider2 = ttk.Scale(master=menu_frame, orient='vertical')

check_var = tk.IntVar(value=0)
check_var2 = tk.IntVar(value=0)
toggle_frame = ttk.Frame(menu_frame)
menu_toggle1 = ttk.Checkbutton(toggle_frame, text='check 1', offvalue=0, onvalue=1, variable=check_var)
menu_toggle2 = ttk.Checkbutton(toggle_frame, text='check 2', offvalue=0, onvalue=1, variable=check_var2)

# Menu layout
menu_frame.columnconfigure(0, weight=1, uniform='a')
menu_frame.columnconfigure(1, weight=1, uniform='a')
menu_frame.columnconfigure(2, weight=1, uniform='a')

menu_frame.rowconfigure(0, weight=1, uniform='a')
menu_frame.rowconfigure(1, weight=1, uniform='a')
menu_frame.rowconfigure(2, weight=1, uniform='a')
menu_frame.rowconfigure(3, weight=1, uniform='a')
menu_frame.rowconfigure(4, weight=1, uniform='a')


menu_button1.grid(row=0, column=0, sticky='nswe', columnspan=2)
menu_button2.grid(row=0, column=2, sticky='nswe', columnspan=2)
menu_button3.grid(row=1, column=0, sticky='nswe', columnspan=3)

# placing sliders
menu_slider1.grid(row=2, column=0, rowspan=2, sticky='nswe', pady=20)
menu_slider2.grid(row=2, column=2, rowspan=2, sticky='nswe', pady=20)

toggle_frame.grid(row=4, column=0, sticky='nswe', columnspan=3)
menu_toggle1.pack(side='left', expand=True)
menu_toggle2.pack(side='left', expand=True)


window.mainloop()