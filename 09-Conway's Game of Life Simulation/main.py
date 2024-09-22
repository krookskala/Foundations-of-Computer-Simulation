from random import randrange
from tkinter import *
import pygame
import sys

class Grid:
    def __init__(self, res):
        width = pygame.display.get_window_size()[0]
        height = pygame.display.get_window_size()[1]
        self.res = res

        self.lower_bound = 2
        self.upper_bound = 3
        self.come_to_life = 3
        self.cells = [[randrange(2) for x in range(int(width / res))] for y in range(int(height / res))]

    def count_neighbors(self, i, j):
        neighbors = 0
        col = len(self.cells[0])
        row = len(self.cells)
        for x in range(-1, 2):
            for y in range(-1, 2):
                neighbors += self.cells[(i + x) % col][(j + y) % row]
        neighbors -= self.cells[i][j]
        return neighbors

    def draw(self, surface):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                color = (255, 255, 255) if self.cells[i][j] == 1 else (0, 0, 0)
                pygame.draw.rect(surface, color, [i * self.res, j * self.res, self.res, self.res])

    def process(self):
        next_gen = [[0 for _ in range(len(self.cells[0]))] for _ in range(len(self.cells))]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                neighbors = self.count_neighbors(i, j)
                self.apply_rule(i, j, neighbors, next_gen)
        self.cells = next_gen

    def apply_rule(self, i, j, neighbors, next_gen):
        if (neighbors < self.lower_bound or neighbors > self.upper_bound) and self.cells[i][j] == 1:
            next_gen[i][j] = 0
        elif neighbors == self.come_to_life and self.cells[i][j] == 0:
            next_gen[i][j] = 1
        else:
            next_gen[i][j] = self.cells[i][j]

    def set_rules(self, lower_bound, upper_bound, come_to_life):
        self.lower_bound = int(lower_bound)
        self.upper_bound = int(upper_bound)
        self.come_to_life = int(come_to_life)

screen_width = 800
screen_height = 800
res = 10
x1 = 400
y1 = 400

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    surface = pygame.Surface(screen.get_size()).convert()
    grid = Grid(res)

    root = Tk()
    root.geometry(f"{x1}x{x1}")
    root.title("Change Rules!")

    def get_value():
        try:
            lower_bound = int(text_area1.get())
            upper_bound = int(text_area2.get())
            alive = int(text_area3.get())
            if lower_bound <= upper_bound:
                display_info['text'] = f"{lower_bound}{upper_bound}/{alive}"
                grid.set_rules(lower_bound, upper_bound, alive)
                error_label['text'] = ''
            else:
                error_label['text'] = 'Error: Lower Bound Cannot Be Greater Than Upper Bound!'
        except ValueError:
            error_label['text'] = 'Error: Please Enter Valid Integers'

    text_area1 = StringVar()
    text_area2 = StringVar()
    text_area3 = StringVar()

    info = Label(root, text="Current Rules: ", font='Helvetica 18 bold')
    info.place(x=1, y=30)
    error_label = Label(root, text="", font='Helvetica 11 bold', fg='red')
    error_label.place(x=1, y=y1 / 2 + 50)
    display_info = Label(root, text="23/3", font='Helvetica 18 bold', fg='#0000FF')
    display_info.place(x=200, y=30)

    Label(root, text="Lower Bound").place(x=1, y=90)
    Label(root, text="Upper Bound").place(x=1, y=120)
    Label(root, text="Come Alive").place(x=1, y=150)

    Entry(root, textvariable=text_area1, width=30).place(x=x1 / 2, y=90)
    Entry(root, textvariable=text_area2, width=30).place(x=x1 / 2, y=120)
    Entry(root, textvariable=text_area3, width=30).place(x=x1 / 2, y=150)

    Button(root, text="Submit", command=get_value, bg="green").place(x=x1 / 2, y=y1 / 2)
    main_dialog = Frame(root)
    main_dialog.pack()

    while True:
        try:
            main_dialog.update()
        except:
            pass
        clock.tick(40)
        grid.draw(surface)
        grid.process()
        screen.blit(surface, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
