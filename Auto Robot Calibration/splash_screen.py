import customtkinter as ctk
from PIL import Image

class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Petrov Engineering")

        self.height = 350
        self.width = 350
        self.x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

        self.overrideredirect(True)

        self.SplashLabel = ctk.CTkLabel(self,
                                        text='',
                                        image=ctk.CTkImage(light_image=Image.open('Images/logo-color.png'),
                                                           dark_image=Image.open('Images/logo-color.png'),
                                                           size=(self.width, self.height)))

        self.SplashLabel.pack(fill='both', expand=True)


splash_screen = SplashScreen()
splash_screen.mainloop()