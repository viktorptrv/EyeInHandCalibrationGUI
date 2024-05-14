import customtkinter as ctk


class CamIPEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='Camera IP')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=100)
        # self.configure(fg_color='#ffba33')
        # self.configure(text_color='black')


class CamPortEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='Port')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=60)
        # self.configure(fg_color='#ffba33')
        # self.configure(text_color='black')


class RobIPEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='Robot IP')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=100)
        # self.configure(fg_color='#ffba33')
        # self.configure(text_color='black')


class RobPortEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='Port')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=60)
        # self.configure(fg_color='#ffba33')
        # self.configure(text_color='black')


class RobUFEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='UF')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=40)


class RobTFEntry(ctk.CTkEntry):
    def __init__(self, parent):
        super().__init__(parent)

        self.configure(placeholder_text='TF')
        self.configure(placeholder_text_color='black')
        self.configure(fg_color='#ffba33')
        self.configure(width=40)