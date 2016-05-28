##########################
#                        #
#  Javier Cabero Guerra  #
#  Copyright (c) 2016    #
#  All rights reserved   #
#                        #
##########################

from sense_hat import SenseHat
import os
import sys
import time
import random
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
        self.pos    = [3, 2]
        self.color  = [0, 0, 50]

    # returns the list of pixels in their absolute position
    def get_abs_pixels(self):
        abs_pixels = []
        for pixel in self.pixels:
            abs_pixels.append([x + y for x, y in zip(pixel, self.pos)])
        return abs_pixels

    def move_left(self, grid):
        for pixel in self.get_abs_pixels():
            if pixel[0] <= 0:
                return False
            if not grid.isEmpty(pixel[1], pixel[0]-1):
                return False
        self.pos[0] = self.pos[0] - 1
        return True

    def move_right(self, grid):
        for pixel in self.get_abs_pixels():
            if pixel[0] >= 7:
                return False
            if not grid.isEmpty(pixel[1], pixel[0]+1):
                return False
        self.pos[0] = self.pos[0] + 1
        return True

    def move_bottom(self, grid):
        
        for pixel in self.get_abs_pixels():
            if pixel[1] >= 7:
                return False
            if not grid.isEmpty(pixel[1]+1, pixel[0]):
                return False

        self.pos[1] = self.pos[1] + 1
        return True

    def draw(self):
        set_pixels(self.get_abs_pixels(), self.color)

    def rotate(self, grid):
        # switch to next rotation
        next_rotation_idx = (self.rotation_idx + 1) % len(self.rotations)

        abs_pixels = []
        for pixel in self.rotations[next_rotation_idx]:
            abs_pixels.append([x + y for x, y in zip(pixel, self.pos)])

        print 'next rotation'
        print abs_pixels

        for abs_pixel in abs_pixels:
            print 'checking room for (' + str(abs_pixel[1]) + ', ' + str(abs_pixel[0]) + ')'
            if (abs_pixel[0] < 0 or 8 <= abs_pixel[0] or 8 <= abs_pixel[1]) or not grid.isEmpty(abs_pixel[1], abs_pixel[0]):
                print 'cant rotate (pixel colliding)'
                print abs_pixel
                return False
            else:
                print 'ok'
        self.rotation_idx = next_rotation_idx
        self.pixels = self.rotations[self.rotation_idx]
        return True

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
            if self.rotate(grid):
                sense.clear(0,0,0)
                self.draw()
                grid.draw() 

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
        self.rotations = [ 
                           [[0, 0], [-1, 0], [0, -1], [1, 0]],
                           [[0, 0], [0, -1], [1,  0], [0, 1]],
                           [[0, 0], [-1, 0], [0,  1], [1, 0]],
                           [[0, 0], [0, -1], [-1, 0], [0, 1]]
                         ]
        self.rotation_idx = 0
        self.pixels       = self.rotations[self.rotation_idx]
        self.color        = [0, 0, 50]
        self.pos          = [3, 1]
            

class Square(Piece):
    def __init__(self):
        self.rotations    = [
                              [[0, 0], [0, 1], [1, 0], [1, 1]]
                            ]
        self.rotation_idx = 0
        self.pixels       = self.rotations[self.rotation_idx]
        self.color        = [50, 0, 50]
        self.pos          = [3, 0]


class RightL(Piece):
    def __init__(self):
        self.rotations    = [
                              [[0,  -1], [0,  0], [0, 1], [1,  1]],
                              [[-1,  1], [-1, 0], [0, 0], [1,  0]],
                              [[-1, -1], [0, -1], [0, 0], [0,  1]],
                              [[-1,  0], [0,  0], [1, 0], [1, -1]]
                            ]
        self.rotation_idx = 0
        self.pixels       = self.rotations[self.rotation_idx]
        self.color        = [50, 0, 0]
        self.pos          = [3, 0]

class LeftL(Piece):
    def __init__(self):
        self.rotations    = [
                              [[0,  -1], [0,  0], [0, 1], [-1, 1]],
                              [[-1, -1], [-1, 0], [0, 0], [1,  0]],
                              [[1,  -1], [0, -1], [0, 0], [0,  1]],
                              [[-1,  0], [0,  0], [1, 0], [1,  1]]
                            ]
        self.rotation_idx = 0
        self.pixels       = self.rotations[self.rotation_idx]
        self.color        = [50, 50, 0]
        self.pos          = [4, 0]

class Bar(Piece):
    def __init__(self):
        self.rotations    = [
                              [[0, -1], [0, 0], [0, 1], [0, 2]],
                              [[-1, 0], [0, 0], [1, 0], [2, 0]]
                            ]
        self.rotation_idx = 0
        self.pixels       = self.rotations[self.rotation_idx]
        self.color        = [0, 50, 0]
        self.pos          = [4, 0]

def random_piece(): 
    n = random.randint(0, 4)
    if n == 0:
        return Triangle()
    elif n == 1:
        return Square()
    elif n == 2:
        return RightL()
    elif n == 3:
        return LeftL()
    elif n == 4:
        return Bar()

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
        for pixel in piece.get_abs_pixels():
            if pixel[0] < 0 or self.width <= pixel[0] or pixel[1] < 0 or self.height <= pixel[1]: continue
            if self.cells[pixel[1]][pixel[0]] != None:
                print 'Tried to add piece to non-empty cell'
                print pixel
                raise 
            self.cells[pixel[1]][pixel[0]] = piece.color

    def check_game_over(self):
        for j in range(self.width):
            if not self.isEmpty(0, j):
                sense.show_message("Game Over")
                sys.exit(0) # TODO move to the piece spawning

    def check_full_lines(self):
        i = self.height-1

        while i >= 0:

            line_complete = True
            for j in range(self.width):
                if self.isEmpty(i, j):
                    line_complete = False
                    break

            # if complete break line and move everything downwards
            if line_complete:
                print self.cells[i]
                for x in range(0, i+1)[::-1]:
                    self.cells[x] = self.cells[x-1]
                self.cells[0] = [None] * self.width
                i = i + 1

            i = i - 1


    def check_lines(self):
        self.check_full_lines()

    def draw(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] != None:
                    sense.set_pixel(j, i, self.cells[i][j])

def set_pixels(pixels, col):
    for p in pixels:
        if 0 <= p[0] and p[0] < 8 and 0 <= p[1] and p[1] < 8:
            sense.set_pixel(p[0], p[1], col[0], col[1], col[2])


def main():
    
    running = True

    global moving_piece
    moving_piece = random_piece()
    moving_piece.draw()

    # time control
    last_time = time.clock()

    step_time          = 1
    respawn_piece_time = 1

    # grid
    grid = Grid(8, 8)

    next_piece_respawn = -1

    #sense.show_message("Tetris")

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

            print 'current grid'
            for i in range(grid.height):
                for j in range(grid.width):
                    if grid.cells[i][j] != None:
                        print 'X',
                    else:
                        print '0',
                print ''
            print ''

            for i in range(grid.height):
                for j in range(grid.width):
                    if not grid.isEmpty(i, j):
                        print 'X',
                    else:
                        print '0',
                print ''

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