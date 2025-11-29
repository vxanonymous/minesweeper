import tkinter as tk
from tkinter import messagebox
import time

from leaderboard.leaderboard import update_leaderboard
from utils.helpers import format_time
from logic.generation import place_mines_safely, count_adjacent_mines

class ClassicGameBoard(tk.Toplevel):
    def __init__(self, controller, width, height, mines, difficulty):
        super().__init__()
        self.controller = controller
        self.width = width
        self.height = height
        self.initial_mines_count = mines 
        self.mines_count = mines 
        self.difficulty = difficulty

        self.title(f"Classic Game - {self.difficulty}")
        self.resizable(False, False)
        self.configure(bg="lightgrey")

        self.is_game_over = False
        self.first_click_done = False
        self.start_time = None
        self.timer_id = None
        self.m_key_pressed = False

        top_frame = tk.Frame(self, bg=self.cget('bg'))
        top_frame.pack(side="top", fill="x", pady=5)

        self.mine_label = tk.Label(top_frame, text=f"Mines: {self.mines_count}", bg=top_frame.cget('bg'))
        self.mine_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(top_frame, text="Time: 0.00", bg=top_frame.cget('bg'))
        self.timer_label.pack(side="right", padx=10)

        self.board_frame = tk.Frame(self, bg=self.cget('bg'))
        self.board_frame.pack()

        self.board = []
        for r in range(height):
            row = []
            for c in range(width):
                cell = {
                    "button": None, "is_mine": False, "adjacent_mines": 0,
                    "is_revealed": False, "is_flagged": False
                }
                row.append(cell)
            self.board.append(row)

        for r_idx in range(height): 
            for c_idx in range(width):
                btn = tk.Button(self.board_frame, width=2, height=1, relief="raised",
                                command=lambda r=r_idx, c=c_idx: self.on_left_click(r, c))
                btn.grid(row=r_idx, column=c_idx)
                btn.bind("<Button-1>", lambda e: self.focus_set())
                
                right_click_handler = lambda event, r=r_idx, c=c_idx: self.on_right_click(r, c)
                btn.bind("<Button-3>", right_click_handler)      
                btn.bind("<Button-2>", right_click_handler)      
                btn.bind("<Control-Button-1>", right_click_handler) 

                self.board[r_idx][c_idx]["button"] = btn

        self.focus_set()
        self.bind("<KeyPress-m>", lambda e: setattr(self, 'm_key_pressed', True))
        self.bind("<KeyRelease-m>", lambda e: setattr(self, 'm_key_pressed', False))
        self.bind("<KeyPress-M>", lambda e: setattr(self, 'm_key_pressed', True))
        self.bind("<KeyRelease-M>", lambda e: setattr(self, 'm_key_pressed', False))

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.destroy()

    def on_left_click(self, r, c):
        if self.m_key_pressed:
            self.on_right_click(r, c)
            return
        
        cell_data = self.board[r][c] 

        if self.is_game_over or cell_data["is_revealed"]:
            return
        
        if cell_data["is_flagged"]:
            return

        if not self.first_click_done:
            self.first_click_done = True
            self.mines_count = place_mines_safely(self.board, self.width, self.height, self.initial_mines_count, r, c)
            flagged_count = sum(item["is_flagged"] for row_board in self.board for item in row_board)
            self.mine_label.config(text=f"Mines: {self.mines_count - flagged_count}")
            
            for rr_init in range(self.height):
                for cc_init in range(self.width):
                    if not self.board[rr_init][cc_init]["is_mine"]:
                        self.board[rr_init][cc_init]["adjacent_mines"] = count_adjacent_mines(self.board, rr_init, cc_init)
            self.start_time = time.time()
            self.update_timer()

        if cell_data["is_mine"]:
            self.reveal_mine(r, c, exploded=True)
            self.game_over(False)
        else:
            self.reveal_cells(r, c)
            if self.check_win():
                self.game_over(True)

    def on_right_click(self, r, c):
        if self.is_game_over or self.board[r][c]["is_revealed"]:
            return
        
        cell = self.board[r][c]
        cell["is_flagged"] = not cell["is_flagged"] 
        
        if cell["is_flagged"]:
            cell["button"].config(text="F", fg="red")
        else:
            cell["button"].config(text="", fg="black")

        if self.first_click_done: 
            flagged_count = sum(item["is_flagged"] for row_board in self.board for item in row_board)
            mines_left = self.mines_count - flagged_count 
            self.mine_label.config(text=f"Mines: {mines_left}")
    
    def reveal_cells(self, r, c):
        stack = [(r, c)]
        visited = set()
        while stack:
            rr, cc = stack.pop()
            if (rr, cc) in visited or self.board[rr][cc]["is_revealed"] or self.board[rr][cc]["is_flagged"]:
                continue
            visited.add((rr, cc))
            cell = self.board[rr][cc]
            cell["is_revealed"] = True
            btn = cell["button"]
            adj = cell["adjacent_mines"]
            colors = ["", "blue", "green", "red", "darkblue", "maroon", "teal", "black", "gray"]
            text_color = colors[adj] if 0 < adj < len(colors) else "black"
            btn.config(relief="sunken", state="disabled", text=str(adj) if adj > 0 else "", disabledforeground=text_color)
            if adj == 0:
                for nr_offset in range(-1, 2):
                    for nc_offset in range(-1, 2):
                        if nr_offset == 0 and nc_offset == 0:
                            continue
                        nr, nc = rr + nr_offset, cc + nc_offset
                        if 0 <= nr < self.height and 0 <= nc < self.width:
                            neighbor = self.board[nr][nc]
                            if not neighbor["is_revealed"] and not neighbor["is_mine"] and not neighbor["is_flagged"]:
                                stack.append((nr, nc))

    def reveal_mine(self, r, c, exploded=False):
        cell = self.board[r][c]
        cell["is_revealed"] = True
        btn = cell["button"]
        if exploded:
            btn.config(text="*", bg="red", fg="white", relief="sunken", state="disabled", disabledforeground="white")
        else:
            btn.config(text="*", bg="lightgrey", relief="sunken", state="disabled", disabledforeground="black")

    def check_win(self):
        for r_idx in range(self.height): 
            for c_idx in range(self.width): 
                cell = self.board[r_idx][c_idx]
                if not cell["is_mine"] and not cell["is_revealed"]:
                    return False
        return True

    def game_over(self, won):
        self.is_game_over = True
        if self.timer_id:
            self.after_cancel(self.timer_id)
        time_taken = time.time() - self.start_time if self.start_time else 0
        if won:
            for r_idx in range(self.height):
                for c_idx in range(self.width):
                    cell = self.board[r_idx][c_idx]
                    if cell["is_mine"] and not cell["is_flagged"]:
                        cell["button"].config(text="F", fg="green", state="disabled", disabledforeground="green")
                    cell["button"].config(state="disabled") 
            messagebox.showinfo("You Win!", f"You cleared the board in {format_time(time_taken)}!")
            if self.difficulty == "Random":
                update_leaderboard("classic", "Random", time_taken,
                                   width=self.width, height=self.height, mines=self.mines_count)
            else:
                update_leaderboard("classic", self.difficulty, time_taken)
        else: 
            for r_idx in range(self.height):
                for c_idx in range(self.width):
                    cell = self.board[r_idx][c_idx]
                    if cell["is_mine"] and not cell["is_revealed"]:
                        if not cell["is_flagged"]:
                            self.reveal_mine(r_idx, c_idx, exploded=False)
                    elif not cell["is_mine"] and cell["is_flagged"]: 
                        cell["button"].config(text="X", bg="lightcoral", fg="black")
                    cell["button"].config(state="disabled")
            messagebox.showinfo("Game Over", "You hit a mine. Better luck next time!")

    def update_timer(self):
        if self.is_game_over:
            return
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.timer_label.config(text=f"Time: {elapsed:.2f}")
        self.timer_id = self.after(100, self.update_timer)