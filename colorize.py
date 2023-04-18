def colorize(text, color, shining=False):
    colors = ("black", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    return f"\033[{'1;5' if shining else 1};{30 + colors.index(color)};0 m{text}\033[0m"
