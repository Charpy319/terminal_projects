import random
import curses

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def random_state(self):
        return [[random.randint(0, 1) for _ in range(0, self.width)] for _ in range(0, self.height)]