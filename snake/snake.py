from collections import deque
import random
import curses

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

WIDTH = 20
HEIGHT = 22

class Snake:
    def __init__(self, init_direction, init_body):
        self.direction = init_direction
        self.body = init_body
        self.last = None

    def take_step(self, pos):
        self.last = self.body.popleft()
        self.body.append(pos)
        return

    def set_direction(self, direction):
        if direction == "w":
            self.direction = UP
        elif direction == "s":
            self.direction = DOWN
        elif direction == "a":
            self.direction = LEFT
        elif direction == "d":
            self.direction = RIGHT
        return self.direction
    
    def head(self):
        return self.body[-1]

    def increase_length(self):
        self.body.appendleft(self.last)
        return

class Apple:
    def __init__(self):
        self.loc = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 4))

    def place_apple(self, snake, matrix, new_apple = True):
        if not new_apple:
            x, y = self.loc
        else:
            coords = set()
            x = random.randint(1, WIDTH - 2)
            y = random.randint(1, HEIGHT - 4)
            for i in range(len(snake)):
                coords.add(snake[i])
                if (x, y) in coords:
                    x = random.randint(1, WIDTH - 2)
                    y = random.randint(1, HEIGHT - 4)
            self.loc = (x, y)
        matrix[y][x] = "*"
        

class Game:
    def __init__(self):
        self.snake = Snake(DOWN, deque([(random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 4))]))
        self.apple = Apple()
        self.points = 0
        self.end = False

    def matrix(self):
        return [[None] * WIDTH for _ in range(HEIGHT - 2)]


    def update(self, key):
        dir_x, dir_y = self.snake.set_direction(key)
        head_x, head_y = self.snake.head()
        new_x, new_y = dir_x + head_x, dir_y + head_y
        self.snake.take_step((new_x, new_y))
        return

    def put_snake(self, matrix, key):
        self.update(key)
        head = self.snake.head()
        head_x, head_y = head
        if head_x == 0:
            head_x = WIDTH - 2
        elif head_x == WIDTH - 1:
            head_x = 1
        if head_y == 0:
            head_y = HEIGHT - 4
        elif head_y == HEIGHT - 3:
            head_y = 1
        body = self.snake.body
        for i in range(len(body) - 1):
            x, y = body[i]
            matrix[y][x] = "0"

        self.snake.body[-1] = (head_x, head_y)
        new_apple = False
        if (head_x, head_y) == self.apple.loc:
            self.points += 1
            self.snake.increase_length()
            new_apple = True
        if matrix[head_y][head_x] == "0":
            self.end = True
        matrix[head_y][head_x] = "x"
        return new_apple

    def render(self, key = None):
        matrix = self.matrix()
        new_apple = self.put_snake(matrix, key)
        self.apple.place_apple(self.snake.body, matrix, new_apple)
        return matrix


game = Game()

def main(stdscr):
    curses.curs_set(0)  # Makes cursor invisible
    stdscr.nodelay(True)    # Keeps code running
    stdscr.timeout(100) # Refresh every 100ms

    while True:
        key = stdscr.getch()
        if key == ord("w"):
            matrix = game.render("w")
        elif key == ord("s"):
            matrix = game.render("s")
        elif key == ord("d"):
            matrix = game.render("d")
        elif key == ord("a"):
            matrix = game.render("a")
        elif key == -1:
            matrix = game.render()
        elif key == ord("q"):
            break
        
        stdscr.clear()
        stdscr.addstr(HEIGHT - 2, 0, "UP: 'w', DOWN: 's', LEFT: 'a', RIGHT: 'd', END: 'q'")
        stdscr.addstr(HEIGHT - 1, 0, f"Score: {game.points}")
        for i in range(HEIGHT - 2):
            for j in range(WIDTH):
                if matrix[i][j] == "*":
                    stdscr.addstr(i, j, "*")
                elif matrix[i][j] == "0":
                    stdscr.addstr(i, j, "0")
                elif matrix[i][j] == "x":
                    stdscr.addstr(i, j, "x")
                elif i == 0 or i == HEIGHT - 3:
                    if j == 0:
                        stdscr.addstr(i, j, "+")
                    elif j == WIDTH - 1:
                        stdscr.addstr(i, j, "+\n")
                    else:
                        stdscr.addstr(i, j, "-")
                else:
                    if j == 0:
                        stdscr.addstr(i, j, "|")
                    elif j == WIDTH - 1:
                        stdscr.addstr(i, j, "|\n")
                    else:
                       stdscr.addstr(i, j, " ")
        stdscr.refresh()
        if game.end:
            stdscr.nodelay(False)
            stdscr.addstr(HEIGHT - 2, 0, f"Score: {game.points}")
            stdscr.addstr(HEIGHT - 1, 0, "Press 'return' to retry and 'q' to quit")
            key = stdscr.getch()
            if key == curses.KEY_ENTER:
                curses.wrapper(main)
            elif key == ord('q'):
                break

curses.wrapper(main)