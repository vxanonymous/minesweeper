# Minesweeper Game

A simple but comprehensive Minesweeper application built with Python and Tkinter, with multiple game modes including Classic, Custom, and Hexagonal variations.

## Features

- **Game Modes:**
  - Classic Mode: Traditional square grid minesweeper
  - Custom Mode: Create own board size and mine count
  - Hexagon Mode: Play on a hexagonal grid

- **Multiple Difficulty Levels:**
  - Beginner, Intermediate, Expert
  - Random configurations

- **Leaderboard:**
  - Track top scores for each mode and difficulty locally
  - Separate leaderboards for Classic, Hexagon, and Custom modes
  - Persistent storage using JSON

- **Controls:**
  - Left-click to reveal cells
  - Right-click or M + Left-click to flag/unflag mines

- **Game Features:**
  - Safe first click
  - Timer tracking
  - Mine counter with flag tracking
  - Color-coded numbers for adjacent mine counts
  - Win/loss detection with game over screens

## Requirements

- Python 3.7 or higher and tkinter

## How to Run
```bash
python main.py
```

```bash
cd /path/to/minesweeper
python main.py
```

## Game Modes

### Classic Mode

Traditional rectangular grid minesweeper with preset difficulties:

- **Beginner:** 9x9 grid with 10 mines
- **Intermediate:** 16x16 grid with 40 mines
- **Expert:** 30x16 grid with 99 mines
- **Random:** Randomly generated board size and mine count

### Custom Mode

- Board width: 10-30 cells
- Board height: 10-30 cells
- Mine count: Minimum 10, maximum depends on board size

### Hexagon Mode

Play on a hexagonal grid with different rules:

- **Beginner:** 8x8 grid with 10 mines
- **Intermediate:** 12x12 grid with 25 mines
- **Expert:** 16x16 grid with 60 mines
- **Random:** Random hexagonal board

## Controls

### Basic Controls

- **Left-click:** Reveal a cell
- **Right-click:** Flag/unflag a mine
- **M + Left-click:** Alternative way to flag/unflag

## Project Structure

```
minesweeper/
├── main.py                          # Main application entry point
├── start_menu.py                    # Start menu screen
├── about_us.py                      # About screen
├── classic_mode/
│   ├── classic_game.py             # Classic game implementation
│   ├── classic_menu.py             # Classic mode menu
│   └── classic_leaderboard_display.py
├── custom_mode/
│   ├── custom_game.py              # Custom game implementation
│   ├── custom_menu.py              # Custom mode menu
│   └── custom_leaderboard_display.py
├── hexagon_mode/
│   ├── hex_game.py                 # Hexagon game implementation
│   ├── hex_menu.py                 # Hexagon mode menu
│   └── hex_leaderboard_display.py
├── leaderboard/
│   ├── leaderboard.py              # Leaderboard logic
│   └── leaderboard_data.json       # Leaderboard storage (auto-generated)
├── logic/
│   └── generation.py               # Mine placement and adjacency logic
└── utils/
    └── helpers.py                  # Utility functions
```

## License

This project is licensed under the MIT License

Developed by Vinh Nguyen
