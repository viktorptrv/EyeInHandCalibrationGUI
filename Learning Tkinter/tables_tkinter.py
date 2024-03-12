import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.geometry('700x800')
window.title('Treeview')

first_names = ['Bob', 'Maria', 'Alex', 'Susan']
last_names = ['Smith', 'Brown', 'Wilson', 'Cook']

# Treeview widget
table = ttk.Treeview(master=window,
                     columns=('first', 'last', 'email'),
                     show='headings')
# adding headings to each column
table.heading('first', text='First name')
table.heading('last', text="Last name")
table.heading('email', text='Email')

# inserting values into a table
# table.insert(parent='', index = 0, values = ('John', 'Doe','gosho@gmail.com'))

for i in range(len(first_names)):
    table.insert(parent='', index=i, values=[first_names[i],
                                             last_names[i],
                                             f'{first_names[i]}.{last_names[i]}@abv.bg'])

table.pack(fill='both', expand=True)

# events
table.bind('<<Treeview')
window.mainloop()