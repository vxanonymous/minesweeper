import tkinter as tk
from leaderboard.leaderboard import load_leaderboard

class CustomLeaderboardDisplay(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.configure(bg=self.cget('bg'))

        label = tk.Label(self, text="Custom Mode Leaderboard", font=("Arial", 16, "bold"), bg=self.cget('bg'))
        label.pack(pady=10)

        self.records_frame = tk.Frame(self, bg=self.cget('bg'))
        self.records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        back_button = tk.Button(
            self, text="Back", command=lambda: controller.show_frame("CustomMenu")
        )
        back_button.pack(pady=10)
        self.update_display() # Initial display

    def update_display(self):
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        data = load_leaderboard()
        records = data.get("custom_mode", {}).get("records", [])

        title_label = tk.Label(self.records_frame, text="Top 10 Scores", font=("Arial", 12, "bold"), bg=self.records_frame.cget('bg'))
        title_label.pack(pady=(5,10))

        if not records:
            tk.Label(self.records_frame, text="No records yet.", bg=self.records_frame.cget('bg')).pack()
            return

        table_frame = tk.Frame(self.records_frame, bg=self.records_frame.cget('bg'))
        table_frame.pack(fill=tk.X)
        
        # Headers
        tk.Label(table_frame, text="#", font=("Arial", 10, "bold"), width=3, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=0, sticky='e', padx=(0,5))
        tk.Label(table_frame, text="Name", font=("Arial", 10, "bold"), width=15, bg=table_frame.cget('bg'), anchor='w').grid(row=0, column=1, sticky='w')
        tk.Label(table_frame, text="Config", font=("Arial", 10, "bold"), width=20, bg=table_frame.cget('bg'), anchor='w').grid(row=0, column=2, sticky='w', padx=5)
        tk.Label(table_frame, text="Mine %", font=("Arial", 10, "bold"), width=8, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=3, sticky='e', padx=5)
        tk.Label(table_frame, text="Time (s)", font=("Arial", 10, "bold"), width=10, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=4, sticky='e', padx=5)
        table_frame.grid_columnconfigure(1, weight=1) # Allow Name to expand
        table_frame.grid_columnconfigure(2, weight=1) # Allow Config to expand


        for i, record in enumerate(records):
            rank_text = f"{i+1}."
            tk.Label(table_frame, text=rank_text, width=3, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=0, sticky='e', padx=(0,5), pady=2)
            tk.Label(table_frame, text=record["name"], width=15, bg=table_frame.cget('bg'), anchor='w', wraplength=120).grid(row=i+1, column=1, sticky='w', pady=2)
            
            config_text = record.get("config", "N/A")
            tk.Label(table_frame, text=config_text, width=20, bg=table_frame.cget('bg'), anchor='w', wraplength=150).grid(row=i+1, column=2, sticky='w', padx=5, pady=2)
            
            perc_str = f"{record.get('mine_percentage', 0) * 100:.1f}%" # Added .get for safety
            tk.Label(table_frame, text=perc_str, width=8, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=3, sticky='e', padx=5, pady=2)
            tk.Label(table_frame, text=f"{record.get('time', 0):.2f}", width=10, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=4, sticky='e', padx=5, pady=2)