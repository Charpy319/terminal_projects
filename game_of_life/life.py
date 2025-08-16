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
    elif key == ord('i'):
        with open("glider.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('g'):
        with open("gun.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('p'):
        with open("pulsar.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('d'):
        with open("pentadec.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines
    elif key == ord('o'):
        with open("door.txt", "r") as f:
            lines = [line.strip() for line in f.readlines()]
        return lines



def main(stdscr):
    configs = {ord('r'), ord('t'), ord('b'), ord('l'), ord('i'), ord('g'), ord('p'), ord('d'), ord('o')}
    stdscr.addstr(0, 0, "Please make your terminal it's maximum size and press enter")
    while stdscr.getch() not in {10, 13, curses.KEY_ENTER}:
        continue
    stdscr.clear()
    stdscr.addstr(0, 0, "Choose your configuration: RANDOM: 'r', TOAD: 't', BEACON: 'b', BLINKER: 'l', GLIDER: 'i', GOSPER GLIDER GUN: 'g', PULSAR: 'p', PENTADECATHLON: 'd', DOOR: 'o'")
    key = stdscr.getch()
    while True:
        if key in configs:
            lines = read_files(key)
            break
        key = stdscr.getch()
    stdscr.clear()
    h_max, w_max = stdscr.getmaxyx()
    if lines:
        game_width, game_height = len(lines[0]), len(lines)
        width, height = game_width + 2, game_height + 4
        start_x, start_y = (w_max - width) // 2, (h_max - height) // 2
        board = Board(game_width, game_height, lines)
    else:
        height, width = h_max, w_max
        width -= 1  # To fit in newline
        game_height, game_width = height - 4, width - 2
        start_x, start_y = 0, 0
        board = Board(game_width, game_height)
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.timeout(300)

    while True:
        stdscr.clear()
        matrix = board.next_state()
        for i in range(height - 2):
            for j in range(width):
                if i == 0 or i == height - 3:
                    if j == 0:
                        stdscr.addstr(start_y + i, start_x + j, "+")
                    elif j == width - 1:
                        stdscr.addstr(start_y + i, start_x + j, "+\n")
                    else:
                        stdscr.addstr(start_y + i, start_x + j, "-")
                else:
                    if j == 0:
                        stdscr.addstr(start_y + i, start_x + j, "|")
                    elif j == width - 1:
                        stdscr.addstr(start_y + i, start_x + j, "|\n")
                    elif matrix[i - 1][j - 1] == 1:
                        stdscr.addstr(start_y + i, start_x + j, "#")
                    else:
                        stdscr.addstr(start_y + i, start_x + j, " ")
        config = "Change your configuration: RANDOM: 'r', TOAD: 't', BEACON: 'b', BLINKER: 'l', GLIDER: 'i', GOSPER GLIDER GUN: 'g', PULSAR: 'p', PENTADECATHLON: 'd', DOOR: 'o'"
        _exit = "Press 'q' to exit"
        stdscr.addstr(start_y + height - 2, (w_max - len(config))// 2, config)
        stdscr.addstr(start_y + height - 1, (w_max - len(_exit)) // 2, _exit)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key in configs:
            lines = read_files(key)
            if lines:
                game_width, game_height = len(lines[0]), len(lines)
                width, height = game_width + 2, game_height + 4
                start_x, start_y = (w_max - width) // 2, (h_max - height) // 2
                board = Board(game_width, game_height, lines)
            else:
                height, width = h_max, w_max
                width -= 1  # To fit in newline
                game_height, game_width = height - 4, width - 2
                start_x, start_y = 0, 0
                board = Board(game_width, game_height)
            stdscr.nodelay(True)
            curses.curs_set(0)
            stdscr.timeout(150)


curses.wrapper(main)