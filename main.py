import tkinter as tk

from start_menu import StartMenu
from about_us import AboutUs

# Classic
from classic_mode.classic_menu import ClassicMenu
from classic_mode.classic_leaderboard_display import ClassicLeaderboardDisplay

# Custom
from custom_mode.custom_menu import CustomMenu
from custom_mode.custom_leaderboard_display import CustomLeaderboardDisplay

# Hex
from hexagon_mode.hex_menu import HexMenu
from hexagon_mode.hex_leaderboard_display import HexLeaderboardDisplay

class MinesweeperApp(tk.Tk):
    """
    Main application class that creates and stores frames by string keys.
    """
    def __init__(self):
        super().__init__()
        self.title("Minesweeper Application")
        self.configure(bg="lightgrey") 
        self.resizable(False, False)

        container = tk.Frame(self, bg=self.cget('bg')) 
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_frame_name = None 

        frame_classes = {
            "StartMenu": StartMenu,
            "AboutUs": AboutUs,
            "ClassicMenu": ClassicMenu,
            "ClassicLeaderboardDisplay": ClassicLeaderboardDisplay,
            "CustomMenu": CustomMenu,
            "CustomLeaderboardDisplay": CustomLeaderboardDisplay,
            "HexMenu": HexMenu,
            "HexLeaderboardDisplay": HexLeaderboardDisplay,
        }

        for name, FrameClass in frame_classes.items():
            frame = FrameClass(container, self) 
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove() 

        self.show_frame("StartMenu")

    def show_frame(self, frame_name_to_show: str):
        if frame_name_to_show not in self.frames:
            print(f"Error: Frame '{frame_name_to_show}' not found.")
            return

        target_frame = self.frames[frame_name_to_show]

        if hasattr(target_frame, "update_display"):
            target_frame.update_display()

        if self.current_frame_name and self.current_frame_name != frame_name_to_show and self.current_frame_name in self.frames:
            current_frame_instance = self.frames[self.current_frame_name]
            current_frame_instance.grid_remove()
        
        target_frame.grid() 
        target_frame.tkraise()
        
        self.current_frame_name = frame_name_to_show
        
        self.update_idletasks()


def main():
    app = MinesweeperApp()
    app.mainloop()

if __name__ == "__main__":
    main()