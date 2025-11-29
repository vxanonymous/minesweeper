def format_time(seconds):
    """
    Format time in mm:ss.xx for display.
    """
    if seconds is None or seconds < 0:
        seconds = 0 
    m = int(seconds // 60)
    s = seconds % 60
    return f"{m:02d}:{s:05.2f}"