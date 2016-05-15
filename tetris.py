##########################
#                        #
#  Javier Cabero Guerra  #
#  Copyright (c) 2016    #
#  All rights reserved   #
#                        #
##########################

from sense_hat import SenseHat
import os
import time
import pygame
from pygame.locals import *

os.system('export DISPLAY=:0')

pygame.init()
pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()

# create and clear
sense = SenseHat()
sense.clear()

moving_piece = None
fixed_pieces = []

class Piece:
    def __init__(self):
        self.pixels = []
        self.color  = [0, 0, 50]

    def move_left(self, grid):
        for pixel in self.pixels:
            if pixel[0] <= 0:
                return False
        for pixel in self.pixels:
            pixel[0] = pixel[0] - 1
        return True

    def move_right(self, grid):
        for pixel in self.pixels:
            if pixel[0] >= 7:
                return False
        for pixel in self.pixels:
            pixel[0] = pixel[0] + 1
        return True

    def move_bottom(self, grid):
        print 'CHECKING BOTTOM'
        for pixel in self.pixels:
            if pixel[1] >= 7:
                return False
            if not grid.isEmpty(pixel[1]+1, pixel[0]):
                return False
            print pixel
            print grid.cells[pixel[1]+1][pixel[0]]

        for pixel in self.pixels:
            pixel[1] = pixel[1] + 1 # TODO Fix coordinate systems
        return True

    def draw(self):
        set_pixels(self.pixels, self.color)

    def handle_event(self, event, grid):
        if event.key == pygame.K_DOWN:
            if self.move_bottom(grid):
                sense.clear(0,0,0)
                self.draw()
                grid.draw()
        elif event.key == pygame.K_UP:
            pass
        elif event.key == pygame.K_LEFT:
            if self.move_left(grid):
                sense.clear(0,0,0)
                self.draw()
                grid.draw()
        elif event.key == pygame.K_RIGHT:
            if self.move_right(grid):
                sense.clear(0,0,0)
                self.draw()
                grid.draw()
        elif event.key == pygame.K_RETURN:
            pass

    def keyboard_input(self, grid):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    self.handle_event(event, grid)
                #if event.type == KEYUP:
                    #self.handle_event(event)

class Triangle(Piece):
    def __init__(self):
        self.pixels = [[3, 0], [2, 1], [3, 1], [4, 1], [5, 1]]
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
        return self.cells[i][j] == None

    def clear_line(self, i):
        self.cells[i] = [None] * self.width

    def add_piece(self, piece):
        for pixel in piece.pixels:
            self.cells[pixel[1]][pixel[0]] = piece.color

    def check_lines(self):



        for i in range(self.height)[::-1]:

            line_complete = True
            for j in range(self.width):
                if not self.isEmpty(i, j):
                    line_complete = False
                    break

            # if complete break line and move everything downwards
            # TODO Fix
            if line_complete:
                print 'line ' + str(i) + ' full' # TODO Fix
                for x in range(0, i+1)[::-1]:
                    self.cells[x] = self.cells[x-1]
                self.cells[0] = [None] * self.width
            
    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] != None:
                    sense.set_pixel(j, i, self.cells[i][j])

def random_piece(): 
    return Triangle() # TODO make more pieces

def main():
    
    running = True

    global moving_piece
    moving_piece = Triangle()
    moving_piece.draw()

    # time control
    last_time = time.clock()

    step_time          = 1
    respawn_piece_time = 1

    # grid
    grid = Grid(8, 8)

    next_piece_respawn = -1

    # main loop
    while running:
    
        # process input
        if moving_piece != None: moving_piece.keyboard_input(grid)

        # next step
        current_time = time.clock()
        if current_time - step_time > last_time: 
            print 'step!'
            last_time = current_time

            if moving_piece != None and not moving_piece.move_bottom(grid):
                print 'bottom!'
                grid.add_piece(moving_piece)
                moving_piece = None
                
                next_piece_respawn = time.clock() + respawn_piece_time # TODO make respawn

                grid.check_lines()

            # check respawn
            if next_piece_respawn != -1 and next_piece_respawn < time.clock():
                next_piece_respawn = -1
                moving_piece = random_piece()
                moving_piece.draw()

            # redraw
            sense.clear()
            if moving_piece != None: moving_piece.draw()
            grid.draw()

        #clock.tick(30)        

if __name__ == '__main__':
    main()