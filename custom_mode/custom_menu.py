import tkinter as tk
from tkinter import messagebox
from .custom_game import CustomGameBoard

class CustomMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label = tk.Label(self, text="Custom Mode", font=("Arial", 18, "bold"), bg=self.cget('bg'))
        label.pack(pady=10)
        entry_frame_bg = self.cget('bg')

        def add_entry_row(text, min_val, max_val, default=""):
            frame = tk.Frame(self, bg=entry_frame_bg)
            frame.pack(pady=2)
            tk.Label(frame, text=f"{text} ({min_val}-{max_val}):", bg=entry_frame_bg).pack(side="left", padx=5)
            entry = tk.Entry(frame, width=5)
            entry.insert(0, default)
            entry.pack(side="left", padx=5)
            return entry

        self.width_entry = add_entry_row("Width", 10, 30, "10")
        self.height_entry = add_entry_row("Height", 10, 30, "10")
        
        mine_frame = tk.Frame(self, bg=entry_frame_bg)
        mine_frame.pack(pady=2)
        tk.Label(mine_frame, text="Mines (>=10, up to 90%):", bg=entry_frame_bg).pack(side="left", padx=5)
        self.mines_entry = tk.Entry(mine_frame, width=5)
        self.mines_entry.insert(0, "10")
        self.mines_entry.pack(side="left", padx=5)


        start_button = tk.Button(self, text="Start Custom Game", command=self.start_custom_game)
        start_button.pack(pady=10)
        leaderboard_button = tk.Button(
            self, text="View Custom Leaderboard",
            command=lambda: controller.show_frame("CustomLeaderboardDisplay")
        )
        leaderboard_button.pack(pady=5)
        back_button = tk.Button(
            self, text="Back to Menu", command=lambda: controller.show_frame("StartMenu")
        )
        back_button.pack(pady=20)

    def start_custom_game(self):
        try:
            w_str, h_str, m_str = self.width_entry.get(), self.height_entry.get(), self.mines_entry.get()
            if not (w_str and h_str and m_str): raise ValueError("All fields are required.")
            w, h, m = int(w_str), int(h_str), int(m_str)

            if not (10 <= w <= 30 and 10 <= h <= 30):
                raise ValueError("Width/Height must be between 10 and 30.")
            total_tiles = w * h
            if total_tiles == 0: raise ValueError("Board dimensions cannot be zero.")
            
            # Adjusted mine validation
            min_mines = 10
            # Max mines should allow at least a few non-mine cells for first click safety
            # (e.g., 9 for a 3x3 safe area)
            safe_area_cells = 9 
            max_m = total_tiles - safe_area_cells
            if max_m < min_mines : # If board is too small to even satisfy min_mines + safe_area
                 max_m = total_tiles -1 if total_tiles > 0 else 0


            if m < min_mines:
                raise ValueError(f"Mines must be >= {min_mines}.")
            if m > max_m :
                 raise ValueError(f"Mines ({m}) exceed maximum allowed ({max_m}) for a {w}x{h} grid to ensure safe first click.")
            
            CustomGameBoard(self.controller, w, h, m)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))