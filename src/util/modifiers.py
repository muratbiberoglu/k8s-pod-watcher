from enum import Enum


class Modifiers(Enum):
    NORMAL = 0
    BOLD = 1
    DIMMED = 2

    # foreground colors
    RED = "38;5;196"
    GREEN = "38;5;46"
    YELLOW = "38;5;220"

    # background colors
    BRED = "48;5;196"
    BGREEN = "48;5;46"
    BYELLOW = "48;5;220"

    def __str__(self):
        return f"\033[{self.value}m"

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)
