
from sense_hat import SenseHat
import os
import time
import pygame  # See http://www.pygame.org/docs
from pygame.locals import *

os.system('export DISPLAY=:0')

print("Press Escape to quit")
time.sleep(1)

pygame.init()
pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

sense = SenseHat()
sense.clear()  # Blank the LED matrix

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

# 0, 0 = Top left
# 7, 7 = Bottom right
UP_PIXELS = [[3, 0], [4, 0]]
DOWN_PIXELS = [[3, 7], [4, 7]]
LEFT_PIXELS = [[0, 3], [0, 4]]
RIGHT_PIXELS = [[7, 3], [7, 4]]
CENTRE_PIXELS = [[3, 3], [4, 3], [3, 4], [4, 4]]

moving_piece = None
fixed_pieces = []

class Piece:
    def __init__(self):
        self.pixels = []
        self.color  = [0, 0, 50]

    def move_left(self):
        for pixel in self.pixels:
            if pixel[0] <= 0:
                return False
        for pixel in self.pixels:
            pixel[0] = pixel[0] - 1
        return True

    def move_right(self):
        for pixel in self.pixels:
            if pixel[0] >= 7:
                return False
        for pixel in self.pixels:
            pixel[0] = pixel[0] + 1
        return True

    def move_bottom(self):
        for pixel in self.pixels:
            if pixel[1] >= 7:
                return False
        for pixel in self.pixels:
            pixel[1] = pixel[1] + 1
        return True

    def draw(self):
        set_pixels(self.pixels, self.color)

    def handle_event(self, event, colour):
        if event.key == pygame.K_DOWN:
            if self.move_bottom():
                sense.clear(0,0,0)
                self.draw()
        elif event.key == pygame.K_UP:
            pass
        elif event.key == pygame.K_LEFT:
            if self.move_left():
                sense.clear(0,0,0)
                self.draw()
        elif event.key == pygame.K_RIGHT:
            if self.move_right():
                sense.clear(0,0,0)
                self.draw()
        elif event.key == pygame.K_RETURN:
            pass

    def keyboard_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    self.handle_event(event, WHITE)
                #if event.type == KEYUP:
                    #self.handle_event(event, BLACK)

class Triangle(Piece):
    def __init__(self):
        self.pixels = [[3, 0], [2, 1], [3, 1], [4, 1]]
        self.color  = [0, 0, 50]

def set_pixels(pixels, col):
    for p in pixels:
        sense.set_pixel(p[0], p[1], col[0], col[1], col[2])

class Grid:

    def __init__(self, width, height):
        self.cells = []
        # TODO Improve matrix creation code?
        for i in range(height):
            self.cells.append([None] * width)

        self.width  = width
        self.height = height

    def isEmpty(self, i, j):
        return self.cells[i][j] != None

    def clear_line(self, i):
        self.cells[i] = [None] * self.width

    def add_cells(self, piece):
        pass

    def check_lines(self):
        for i in range(self.height)[::-1]:

            line_complete = True
            for j in range(self.width):
                if not self.isEmpty(i, j):
                    line_complete = False
                    break

            # if complete break line and move everything downwards
            if line_complete:
                for x in range(i, self.height-1)[::-1]:
                    self.cells[x] = self.cells[x-1]
                self.cells[0] = [None] * self.width

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] != None:
                    sense.set_pixel(i, j, self.cells[i][j])

def main():
    
    running = True

    global moving_piece
    moving_piece = Triangle()
    moving_piece.draw()

    # time control
    last_time = time.clock()

    step_time = 1

    # grid
    grid = Grid(8, 8)

    # main loop
    while running:
    
        # process input
        if moving_piece != None: moving_piece.keyboard_input()

        # next step
        current_time = time.clock()
        if current_time - step_time > last_time: 
            print 'step!'
            last_time = current_time

            if not moving_piece.move_bottom():
                print 'bottom!'
                #moving_piece.freeze()
                #check_lines(grid)

            # redraw
            sense.clear()
            moving_piece.draw()
            grid.draw()


    clock.tick(30)                                            
if __name__ == '__main__':
    main()