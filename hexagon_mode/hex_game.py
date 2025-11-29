import tkinter as tk
from tkinter import messagebox
import random
import time
import math 

from leaderboard.leaderboard import update_leaderboard
from utils.helpers import format_time

class HexGameBoard(tk.Toplevel):
    def __init__(self, controller, rows, cols, mines, difficulty):
        super().__init__()
        self.controller = controller
        self.rows = rows
        self.cols = cols
        self.initial_mines_count = mines
        self.mines_count = mines 
        self.difficulty = difficulty

        self.title(f"Hex Minesweeper - {self.difficulty}")
        self.resizable(False, False)
        self.configure(bg="lightgrey")

        self.is_game_over = False
        self.first_click_done = False
        self.start_time = None
        self.timer_id = None
        self.m_key_pressed = False

        self.hex_size = 20

        # Hexagon geometry constants based on self.hex_size (radius R from center to vertex)
        self.R = self.hex_size # Radius from center to vertex
        self.hex_visual_height = 2 * self.R  # For hexagon (distance between parallel horizontal sides)
        self.hex_visual_width = math.sqrt(3) * self.R

        # Canvas padding
        self.canvas_padding_x = self.hex_visual_width / 2 + 5
        self.canvas_padding_y = self.hex_visual_height / 2 + 5


        top_frame = tk.Frame(self, bg=self.cget('bg'))
        top_frame.pack(side="top", fill="x", pady=5)

        self.mine_label = tk.Label(top_frame, text=f"Mines: {mines}", bg=top_frame.cget('bg'))
        self.mine_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(top_frame, text="Time: 0.00", bg=top_frame.cget('bg'))
        self.timer_label.pack(side="right", padx=10)

        # Calculate canvas size
        max_c_idx = self.cols - 1
        canvas_w = self.canvas_padding_x * 2
        if self.cols > 0:
            if self.rows > 0 and (self.rows - 1) % 2 == 1:
                last_hex_center_x = self.R * math.sqrt(3) * (max_c_idx + 0.5)
            else:
                last_hex_center_x = self.R * math.sqrt(3) * max_c_idx
            canvas_w += last_hex_center_x + (self.hex_visual_width / 2)
        else:
            canvas_w = self.canvas_padding_x * 2

        canvas_h = self.canvas_padding_y * 2
        if self.rows > 0:
            last_row_center_y = self.R * 1.5 * (self.rows - 1)
            canvas_h += last_row_center_y + (self.hex_visual_height / 2)
        else:
            canvas_h = self.canvas_padding_y * 2


        self.canvas = tk.Canvas(self, bg="white", width=int(canvas_w), height=int(canvas_h))
        self.canvas.pack()

        self.board = []
        for r in range(rows):
            row_data = []
            for c in range(cols):
                cell = {
                    "is_mine": False, "adj_mines": 0, "is_revealed": False,
                    "is_flagged": False, "polygon_id": None, "text_id": None
                }
                row_data.append(cell)
            self.board.append(row_data)

        self.draw_hex_grid()
        
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

    def get_hex_corners(self, center_x, center_y):
        corners = []
        for i in range(6):
            angle_deg = 60 * i - 30 
            angle_rad = math.pi / 180 * angle_deg
            x = center_x + self.R * math.cos(angle_rad)
            y = center_y + self.R * math.sin(angle_rad)
            corners.extend([x, y])
        return corners

    def get_hex_center(self, r_idx, c_idx):
        """Calculate screen coordinates for the center of a hex at (r_idx, c_idx)."""
        center_x = self.canvas_padding_x + self.R * math.sqrt(3) * (c_idx + 0.5 * (r_idx % 2))
        center_y = self.canvas_padding_y + self.R * 1.5 * r_idx
        return center_x, center_y

    def draw_hex_grid(self):
        for r_idx in range(self.rows): 
            for c_idx in range(self.cols): 
                center_x, center_y = self.get_hex_center(r_idx, c_idx)
                corners = self.get_hex_corners(center_x, center_y)
                poly_id = self.canvas.create_polygon(
                    corners, outline="black", fill="lightgray", activefill="gray", width=1
                )
                self.board[r_idx][c_idx]["polygon_id"] = poly_id
                
                def make_left_handler(r, c):
                    def handler(event):
                        self.focus_set()
                        self.on_left_click(r, c)
                    return handler
                
                hex_left_click_handler = make_left_handler(r_idx, c_idx)
                hex_right_click_handler = lambda event, r=r_idx, c=c_idx: self.on_right_click(r, c)
                
                self.canvas.tag_bind(poly_id, "<Button-1>", hex_left_click_handler)
                self.canvas.tag_bind(poly_id, "<Button-3>", hex_right_click_handler)
                self.canvas.tag_bind(poly_id, "<Button-2>", hex_right_click_handler)
                self.canvas.tag_bind(poly_id, "<Control-Button-1>", hex_right_click_handler)
    
    def place_hex_mines(self, safe_r, safe_c):
        all_coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        safe_zone = set([(safe_r, safe_c)])
        for nr, nc in self.get_hex_neighbors(safe_r, safe_c):
            safe_zone.add((nr, nc))
        possible_mine_coords = [coord for coord in all_coords if coord not in safe_zone]
        random.shuffle(possible_mine_coords)
        
        actual_mines_to_place = min(self.initial_mines_count, len(possible_mine_coords))
        if actual_mines_to_place < 0:
            actual_mines_to_place = 0
        
        # Reset all cells to not be mines first
        for r_loop in range(self.rows):
            for c_loop in range(self.cols):
                self.board[r_loop][c_loop]["is_mine"] = False
                
        for i in range(actual_mines_to_place):
            r_mine, c_mine = possible_mine_coords[i]
            self.board[r_mine][c_mine]["is_mine"] = True
        self.mines_count = actual_mines_to_place

    def calculate_adjacencies(self):
        for r_loop in range(self.rows):
            for c_loop in range(self.cols):
                if not self.board[r_loop][c_loop]["is_mine"]:
                    self.board[r_loop][c_loop]["adj_mines"] = self.count_adj_hex_mines(r_loop, c_loop)

    def get_hex_neighbors(self, r, c): 
        neighbors = []
        if r % 2 == 1:  # Odd rows
            potential_offsets = [(0, -1), (0, 1), (-1, 0), (-1, 1), (1, 0), (1, 1)]
        else:  # Even rows
            potential_offsets = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
        for dr, dc in potential_offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))
        return neighbors

    def count_adj_hex_mines(self, r, c): 
        count = 0
        for nr, nc in self.get_hex_neighbors(r,c):
            if self.board[nr][nc]["is_mine"]:
                count += 1
        return count

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
            self.place_hex_mines(r,c) 
            self.calculate_adjacencies()
            flagged_count = sum(item["is_flagged"] for row in self.board for item in row)
            self.mine_label.config(text=f"Mines: {self.mines_count - flagged_count}")
            self.start_time = time.time()
            self.update_timer()
        
        if cell_data["is_mine"]:
            self.reveal_hex_mine(r, c, exploded=True)
            self.game_over(False)
        else:
            self.flood_fill_hex(r, c)
            if self.check_win():
                self.game_over(True)

    def on_right_click(self, r, c):
        if self.is_game_over or self.board[r][c]["is_revealed"]:
            return
        cell = self.board[r][c]
        cell["is_flagged"] = not cell["is_flagged"]

        if cell["text_id"]:
            self.canvas.delete(cell["text_id"])
            cell["text_id"] = None
        
        if cell["is_flagged"]:
            self.canvas.itemconfig(cell["polygon_id"], fill="pink")
            cx, cy = self.get_hex_center(r, c)
            cell["text_id"] = self.canvas.create_text(cx, cy, text="F", fill="red", font=("Arial", int(self.R*0.6), "bold"))
        else:
            self.canvas.itemconfig(cell["polygon_id"], fill="lightgray")
        
        if self.first_click_done:
            flagged_count = sum(item["is_flagged"] for row in self.board for item in row)
            mines_left = self.mines_count - flagged_count
            self.mine_label.config(text=f"Mines: {mines_left}")
        
    def flood_fill_hex(self, r, c):
        stack = [(r, c)]
        visited = set()
        while stack:
            rr, cc = stack.pop()
            if (rr, cc) in visited or self.board[rr][cc]["is_revealed"] or self.board[rr][cc]["is_flagged"]:
                continue
            visited.add((rr, cc))
            cell = self.board[rr][cc]
            cell["is_revealed"] = True

            if cell["text_id"]:
                self.canvas.delete(cell["text_id"])
                cell["text_id"] = None
            self.canvas.itemconfig(cell["polygon_id"], fill="white", activefill="white")

            adj = cell["adj_mines"]
            if adj > 0:
                cx, cy = self.get_hex_center(rr, cc)
                colors = ["", "blue", "green", "red", "darkblue", "maroon", "teal", "black", "gray"]
                text_color = colors[adj] if 0 < adj < len(colors) else "black"
                cell["text_id"] = self.canvas.create_text(cx, cy, text=str(adj), fill=text_color, font=("Arial", int(self.R*0.7), "bold"))

            self.canvas.tag_unbind(cell["polygon_id"], "<Button-1>")
            self.canvas.tag_unbind(cell["polygon_id"], "<Button-3>")
            self.canvas.tag_unbind(cell["polygon_id"], "<Button-2>")
            self.canvas.tag_unbind(cell["polygon_id"], "<Control-Button-1>")

            if adj == 0:
                for nr, nc in self.get_hex_neighbors(rr, cc):
                    neighbor = self.board[nr][nc]
                    if not neighbor["is_revealed"] and not neighbor["is_mine"] and not neighbor["is_flagged"]:
                        stack.append((nr, nc))
                        
    def reveal_hex_mine(self, r, c, exploded=False):
        cell = self.board[r][c]
        cell["is_revealed"] = True
        if cell["text_id"]:
            self.canvas.delete(cell["text_id"])
            cell["text_id"] = None
        
        fill_color = "red" if exploded else "darkgrey"
        self.canvas.itemconfig(cell["polygon_id"], fill=fill_color, activefill=fill_color)
        cx, cy = self.get_hex_center(r, c)
        cell["text_id"] = self.canvas.create_text(cx, cy, text="*", fill="white" if exploded else "black", font=("Arial", int(self.R*0.8), "bold"))
        self.canvas.tag_unbind(cell["polygon_id"], "<Button-1>")
        self.canvas.tag_unbind(cell["polygon_id"], "<Button-3>")
        self.canvas.tag_unbind(cell["polygon_id"], "<Button-2>")
        self.canvas.tag_unbind(cell["polygon_id"], "<Control-Button-1>")

    def check_win(self):
        for row_board in self.board:
            for cell_item in row_board:
                if not cell_item["is_mine"] and not cell_item["is_revealed"]:
                    return False
        return True

    def game_over(self, won):
        self.is_game_over = True
        if self.timer_id:
            self.after_cancel(self.timer_id)
        elapsed = time.time() - self.start_time if self.start_time else 0

        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                cell = self.board[r_idx][c_idx]
                self.canvas.tag_unbind(cell["polygon_id"], "<Button-1>")
                self.canvas.tag_unbind(cell["polygon_id"], "<Button-3>")
                self.canvas.tag_unbind(cell["polygon_id"], "<Button-2>")
                self.canvas.tag_unbind(cell["polygon_id"], "<Control-Button-1>")
                current_fill = self.canvas.itemcget(cell["polygon_id"], "fill")
                self.canvas.itemconfig(cell["polygon_id"], activefill=current_fill)

        if won:
            for r_idx in range(self.rows):
                for c_idx in range(self.cols):
                    cell = self.board[r_idx][c_idx]
                    if cell["is_mine"] and not cell["is_flagged"]:
                        if cell["text_id"]:
                            self.canvas.delete(cell["text_id"])
                            cell["text_id"] = None
                        cx, cy = self.get_hex_center(r_idx, c_idx)
                        self.canvas.itemconfig(cell["polygon_id"], fill="palegreen") 
                        cell["text_id"] = self.canvas.create_text(cx, cy, text="F", fill="green", font=("Arial", int(self.R*0.6), "bold"))
            messagebox.showinfo("You Win!", f"You cleared the hex board in {format_time(elapsed)}!")
            if self.difficulty == "Random":
                update_leaderboard("hexagon", "Random", elapsed, width=self.cols, height=self.rows, mines=self.mines_count)
            else:
                update_leaderboard("hexagon", self.difficulty, elapsed)
        else: 
            for r_idx in range(self.rows):
                for c_idx in range(self.cols):
                    cell = self.board[r_idx][c_idx]
                    if cell["is_mine"] and not cell["is_revealed"]:
                        if not cell["is_flagged"]:
                            self.reveal_hex_mine(r_idx, c_idx, exploded=False)
                    elif not cell["is_mine"] and cell["is_flagged"]:
                        if cell["text_id"]:
                            self.canvas.delete(cell["text_id"])
                            cell["text_id"] = None
                        cx, cy = self.get_hex_center(r_idx, c_idx)
                        self.canvas.itemconfig(cell["polygon_id"], fill="lightcoral")
                        cell["text_id"] = self.canvas.create_text(cx, cy, text="X", fill="black", font=("Arial", int(self.R*0.6)))
            messagebox.showinfo("Game Over", "You hit a mine in Hex Mode!")

    def update_timer(self):
        if self.is_game_over:
            return
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.timer_label.config(text=f"Time: {elapsed:.2f}")
        self.timer_id = self.after(100, self.update_timer)