import random
import curses

class Board:
    def __init__(self, width, height, text = None):
        self.width = width
        self.height = height
        self.text = text
        self.state = self.initial_state()
        self.neighbours = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
            ]

    def initial_state(self):
        if not self.text:
            return [[random.randint(0, 1) for _ in range(self.width)] for _ in range(self.height)]
        else:
            matrix = [[0 for _ in range(len(self.text[0]))] for _ in range(len(self.text))]
            for i in range(len(self.text)):
                for j in range(len(self.text[0])):
                    if self.text[i][j] == '1':
                        matrix[i][j] = 1
            return matrix

    def next_state(self):
        matrix = self.state
        next_matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                alive_count = 0
                for x, y in self.neighbours:
                    neighbour_x, neighbour_y = j + x, i + y
                    if (0 <= neighbour_y < self.height) and (0 <= neighbour_x < self.width):
                        if matrix[neighbour_y][neighbour_x] == 1:
                            alive_count += 1
                if alive_count == 3:
                    next_matrix[i][j] = 1
                elif alive_count == 2 and matrix[i][j] == 1:
                    next_matrix[i][j] = 1
        self.state = next_matrix
        return next_matrix

def read_files(key):
    if key == ord('r'):
        return None
    elif key == ord('t'):
        with open("toad.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('b'):
        with open("beacon.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('l'):
        with open("blinker.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('d'):
        with open("glider.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('g'):
        with open("gun.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines


def main(stdscr):
    configs = {ord('r'), ord('t'), ord('b'), ord('l'), ord('d'), ord('g')}
    stdscr.addstr(0, 0, "Please make your terminal it's maximum size and press enter")
    while stdscr.getch() not in {10, 13, curses.KEY_ENTER}:
        continue
    stdscr.clear()
    stdscr.addstr(0, 0, "Choose your configuration: RANDOM: 'r', TOAD: 't', BEACON: 'b', BLINKER: 'l', GLIDER: 'd', GOSPER GLIDER GUN: 'g'")
    key = stdscr.getch()
    while True:
        if key in configs:
            lines = read_files(key)
            break
        key = stdscr.getch()
    stdscr.clear()
    if lines != None:
        game_width, game_height = len(lines[0]), len(lines)
        width, height = game_width + 2, game_height + 4
        board = Board(game_width, game_height,