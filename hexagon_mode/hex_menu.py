import tkinter as tk
import random
from tkinter import messagebox
from .hex_game import HexGameBoard

class HexMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label = tk.Label(self, text="Hex Mode", font=("Arial", 18, "bold"), bg=self.cget('bg'))
        label.pack(pady=10)

        tk.Button(
            self, text="Beginner (8x8, 10 mines)",
            command=lambda: self.start_hex_game(8, 8, 10, "Beginner")
        ).pack(pady=5)
        tk.Button(
            self, text="Intermediate (12x12, 25 mines)",
            command=lambda: self.start_hex_game(12, 12, 25, "Intermediate")
        ).pack(pady=5)
        tk.Button(
            self, text="Expert (16x16, 60 mines)",
            command=lambda: self.start_hex_game(16, 16, 60, "Expert")
        ).pack(pady=5)
        tk.Button(
            self, text="Random", command=self.start_random_hex_game
        ).pack(pady=5)
        tk.Button(
            self, text="View Hex Leaderboard",
            command=lambda: controller.show_frame("HexLeaderboardDisplay")
        ).pack(pady=10)
        tk.Button(
            self, text="Back to Menu", command=lambda: controller.show_frame("StartMenu")
        ).pack(pady=20)

    def start_hex_game(self, rows, cols, mines, difficulty):
        HexGameBoard(self.controller, rows, cols, mines, difficulty)

    def start_random_hex_game(self):
        rows = random.randint(6, 20)
        cols = random.randint(6, 20)
        total_cells = rows * cols
        min_m = 5
        
        if total_cells == 0:
            messagebox.showerror("Error", "Board dimensions too small for Hex Random.")
            return

        # Max mines should allow for at least a few non-mine cells for first click safety
        # (e.g., 7 for a hex cell and its 6 neighbors)
        safe_area_cells = 7 
        max_m = total_cells - safe_area_cells
        if max_m < min_m : 
             max_m = total_cells -1 if total_cells > 0 else 0


        if min_m > max_m :
            m = max_m if max_m >=0 else 0 # Ensure mines not negative
        else:
            m = random.randint(min_m, max_m)
            
        if m < 0:
            m = 0

        HexGameBoard(self.controller, rows, cols, m, "Random")