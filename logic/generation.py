import random

def place_mines_safely(board, width, height, mines_count, safe_r, safe_c):
    """
    Randomly places `mines_count` mines on the board,
    ensuring (safe_r, safe_c) and its direct neighbors are NOT mines.
    Returns the actual number of mines placed, which might be less than
    mines_count if the board is too small for the requested number of mines
    plus the safe area.
    """
    safe_zone = set([(safe_r, safe_c)])
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            nr, nc = safe_r + dr, safe_c + dc
            if 0 <= nr < height and 0 <= nc < width:
                safe_zone.add((nr, nc))
    
    possible_mine_coords = []
    for r in range(height):
        for c in range(width):
            if (r, c) not in safe_zone:
                possible_mine_coords.append((r, c))

    random.shuffle(possible_mine_coords)
    
    actual_mines_to_place = min(mines_count, len(possible_mine_coords))
    if actual_mines_to_place < 0:
        actual_mines_to_place = 0


    for i in range(actual_mines_to_place):
        r_mine, c_mine = possible_mine_coords[i]
        board[r_mine][c_mine]["is_mine"] = True
    
    return actual_mines_to_place


def count_adjacent_mines(board, row, col):
    height = len(board)
    width = len(board[0]) if height > 0 else 0
    count = 0
    for rr_offset in range(-1, 2):
        for cc_offset in range(-1, 2):
            if rr_offset == 0 and cc_offset == 0:
                continue
            rr, cc = row + rr_offset, col + cc_offset
            if 0 <= rr < height and 0 <= cc < width and board[rr][cc]["is_mine"]:
                count += 1
    return count