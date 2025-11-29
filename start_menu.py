import tkinter as tk

class StartMenu(tk.Frame):
    """
    The initial menu screen for the Minesweeper application.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white") 
        self.controller = controller

        label = tk.Label(self, text="Minesweeper", font=("Arial", 24, "bold"), bg=self.cget('bg'))
        label.pack(pady=20)

        classic_button = tk.Button(
            self,
            text="Classic",
            width=20,
            height=2,
            command=lambda: controller.show_frame("ClassicMenu")
        )
        classic_button.pack(pady=5)

        custom_button = tk.Button(
            self,
            text="Custom",
            width=20,
            height=2,
            command=lambda: controller.show_frame("CustomMenu")
        )
        custom_button.pack(pady=5)

        hex_button = tk.Button(
            self,
            text="Hexagon",
            width=20,
            height=2,
            command=lambda: controller.show_frame("HexMenu")
        )
        hex_button.pack(pady=5)

        about_button = tk.Button(
            self,
            text="About Us",
            width=20,
            height=2,
            command=lambda: controller.show_frame("AboutUs")
        )
        about_button.pack(pady=5)