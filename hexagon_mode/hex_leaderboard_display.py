import tkinter as tk
from tkinter import ttk
from leaderboard.leaderboard import load_leaderboard

class HexLeaderboardDisplay(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.configure(bg=self.cget('bg'))

        title_label = tk.Label(self, text="Hex Leaderboard", font=("Arial", 16, "bold"), bg=self.cget('bg'))
        title_label.pack(pady=10)
        
        controls_frame = tk.Frame(self, bg=self.cget('bg'))
        controls_frame.pack(pady=5)

        self.difficulty_var = tk.StringVar(value="Beginner")
        diff_options = ["Beginner", "Intermediate", "Expert", "Random"]
        self.diff_combo = ttk.Combobox(controls_frame, textvariable=self.difficulty_var, values=diff_options, state="readonly", width=15)
        self.diff_combo.pack(side=tk.LEFT, padx=5)
        self.diff_combo.bind("<<ComboboxSelected>>", self.update_display)

        self.records_frame = tk.Frame(self, bg=self.cget('bg'))
        self.records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame("HexMenu"))
        back_button.pack(pady=10)
        self.update_display()

    def update_display(self, event=None):
        for widget in self.records_frame.winfo_children():
            widget.destroy()
        difficulty = self.difficulty_var.get()
        data = load_leaderboard()
        hex_data = data.get("hexagon", {})
        records = hex_data.get(difficulty, [])

        difficulty_title_label = tk.Label(self.records_frame, text=f"{difficulty} Scores (Top 10)", font=("Arial", 12, "bold"), bg=self.records_frame.cget('bg'))
        difficulty_title_label.pack(pady=(5,10))

        if not records:
            tk.Label(self.records_frame, text="No records yet.", bg=self.records_frame.cget('bg')).pack()
            return

        table_frame = tk.Frame(self.records_frame, bg=self.records_frame.cget('bg'))
        table_frame.pack(fill=tk.X)

        tk.Label(table_frame, text="#", font=("Arial", 10, "bold"), width=3, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=0, sticky='e', padx=(0,5))
        tk.Label(table_frame, text="Name", font=("Arial", 10, "bold"), width=20, bg=table_frame.cget('bg'), anchor='w').grid(row=0, column=1, sticky='w')
        has_proportion = records and "proportion" in records[0]
        if has_proportion:
            tk.Label(table_frame, text="Prop.", font=("Arial", 10, "bold"), width=8, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=2, sticky='e', padx=5)
            tk.Label(table_frame, text="Time (s)", font=("Arial", 10, "bold"), width=10, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=3, sticky='e', padx=5)
            table_frame.grid_columnconfigure(1, weight=1)
        else:
            tk.Label(table_frame, text="Time (s)", font=("Arial", 10, "bold"), width=12, bg=table_frame.cget('bg'), anchor='e').grid(row=0, column=2, sticky='e', padx=5)
            table_frame.grid_columnconfigure(1, weight=1)
            table_frame.grid_columnconfigure(2, weight=0)

        for i, record in enumerate(records):
            tk.Label(table_frame, text=f"{i+1}.", width=3, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=0, sticky='e', padx=(0,5), pady=2)
            tk.Label(table_frame, text=record["name"], width=20, bg=table_frame.cget('bg'), anchor='w', wraplength=150).grid(row=i+1, column=1, sticky='w', pady=2)
            if has_proportion:
                perc_str = f"{record.get('proportion', 0)*100:.1f}%"
                tk.Label(table_frame, text=perc_str, width=8, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=2, sticky='e', padx=5, pady=2)
                tk.Label(table_frame, text=f"{record.get('time',0):.2f}", width=10, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=3, sticky='e', padx=5, pady=2)
            else:
                tk.Label(table_frame, text=f"{record.get('time',0):.2f}", width=12, bg=table_frame.cget('bg'), anchor='e').grid(row=i+1, column=2, sticky='e', padx=5, pady=2)