import tkinter as tk

class AboutUs(tk.Frame):
    """
    Simple screen to show 'About Us' information and go back to StartMenu.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white") 
        self.controller = controller

        label = tk.Label(self, text="About Us", font=("Arial", 18, "bold"), bg=self.cget('bg'))
        label.pack(pady=10)

        info_text = (
            "This Minesweeper application demonstrates Python and Tkinter,\n"
            "featuring Classic, Custom, and Hexagonal modes,\n"
            "plus multiple leaderboard displays.\n\n"
            "Developed by Vinh Nguyen."
        )

        info_label = tk.Label(self, text=info_text, font=("Arial", 12), bg=self.cget('bg'))
        info_label.pack(pady=10)

        back_button = tk.Button(
            self,
            text="Back to Menu",
            command=lambda: controller.show_frame("StartMenu")
        )
        back_button.pack(pady=20)