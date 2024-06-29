import customtkinter as ctk


class Coords(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Entry1 = ctk.CTkEntry(master=self,
                                   placeholder_text='X=',
                                   width=60)

        self.Entry2 = ctk.CTkEntry(master=self,
                                   placeholder_text='Y=',
                                   width=60)

        self.Entry3 = ctk.CTkEntry(master=self,
                                   placeholder_text='Z=',
                                   width=60)

        self.Entry4 = ctk.CTkEntry(master=self,
                                   placeholder_text='W=',
                                   width=60)

        self.Entry5 = ctk.CTkEntry(master=self,
                                   placeholder_text='P=',
                                   width=60)

        self.Entry6 = ctk.CTkEntry(master=self,
                                   placeholder_text='R=',
                                   width=60)

        self.Entry1.place(relx=0.05, rely=0.1)
        self.Entry2.place(relx=0.2, rely=0.1)
        self.Entry3.place(relx=0.35, rely=0.1)
        self.Entry4.place(relx=0.5, rely=0.1)
        self.Entry5.place(relx=0.65, rely=0.1)
        self.Entry6.place(relx=0.8, rely=0.1)

    # def joints(self):
    #     self.Entry1.configure(placeholder_text='J1')
    #     self.Entry2.configure(placeholder_text='J2')
    #     self.Entry3.configure(placeholder_text='J3')
    #     self.Entry4.configure(placeholder_text='J4')
    #     self.Entry5.configure(placeholder_text='J5')
    #     self.Entry6.configure(placeholder_text='J6')


class JCoords(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.Entry1 = ctk.CTkEntry(master=self,
                                   placeholder_text='J1=',
                                   width=60)

        self.Entry2 = ctk.CTkEntry(master=self,
                                   placeholder_text='J2=',
                                   width=60)

        self.Entry3 = ctk.CTkEntry(master=self,
                                   placeholder_text='J3=',
                                   width=60)

        self.Entry4 = ctk.CTkEntry(master=self,
                                   placeholder_text='J4=',
                                   width=60)

        self.Entry5 = ctk.CTkEntry(master=self,
                                   placeholder_text='J5=',
                                   width=60)

        self.Entry6 = ctk.CTkEntry(master=self,
                                   placeholder_text='J6=',
                                   width=60)
        self.place_widget()

    def place_widget(self):
        self.Entry1.place(relx=0.05, rely=0.1)
        self.Entry2.place(relx=0.2, rely=0.1)
        self.Entry3.place(relx=0.35, rely=0.1)
        self.Entry4.place(relx=0.5, rely=0.1)
        self.Entry5.place(relx=0.65, rely=0.1)
        self.Entry6.place(relx=0.8, rely=0.1)

    def forget_widgets(self):
        self.Entry1.place_forget()
        self.Entry2.place_forget()
        self.Entry3.place_forget()
        self.Entry4.place_forget()
        self.Entry5.place_forget()
        self.Entry6.place_forget()


