__all__ = [
    'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE',
    'colorize', 'printcolored'
]


BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def colorize(text, color):
    return "\x1b[1;%dm" % (30 + color) + text + "\x1b[0m"

def printcolored(text, color=WHITE):
    print(colorize(text, color))
