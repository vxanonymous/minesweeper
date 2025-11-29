import tkinter as tk
import random
from .classic_game import ClassicGameBoard

class ClassicMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        label = tk.Label(self, text="Classic Mode", font=("Arial", 18, "bold"), bg=self.cget('bg'))
        label.pack(pady=10)

        tk.Button(
            self, text="Beginner (9x9, 10 mines)",
            command=lambda: self.start_classic_game(9, 9, 10, "Beginner")
        ).pack(pady=5)
        tk.Button(
            self, text="Intermediate (16x16, 40 mines)",
            command=lambda: self.start_classic_game(16, 16, 40, "Intermediate")
        ).pack(pady=5)
        tk.Button(
            self, text="Expert (30x16, 99 mines)",
            command=lambda: self.start_classic_game(30, 16, 99, "Expert")
        ).pack(pady=5)
        tk.Button(
            self, text="Random", command=self.start_random_game
        ).pack(pady=5)
        tk.Button(
            self, text="View Classic Leaderboard",
            command=lambda: controller.show_frame("ClassicLeaderboardDisplay")
        ).pack(pady=10)
        tk.Button(
            self, text="Back to Menu",
            command=lambda: controller.show_frame("StartMenu")
        ).pack(pady=20)

    def start_classic_game(self, width, height, mines, difficulty):
        ClassicGameBoard(self.controller, width, height, mines, difficulty)

    def start_random_game(self):
        w = random.randint(10, 30)
        h = random.randint(10, 30)
        total_tiles = w * h
        max_m = int(total_tiles * 0.9)
        # Ensure at least 10 mines; also ensure mines < total_tiles - (area for first click safety)
        # For simplicity, if max_m becomes too small, it will be handled by place_mines_safely returning actual count
        min_m = 10
        if max_m < min_m: # If 90% is less than 10 (small board)
            m = min(min_m, total_tiles - 1 if total_tiles > 0 else 0) # Ensure at least 1 non-mine
        else:
            m = random.randint(min_m, max_m)
        
        if m >= total_tiles and total_tiles > 0: # Ensure not all cells are mines
            m = total_tiles -1
        if m < 0:
            m = 0

        ClassicGameBoard(self.controller, w, h, m, "Random")