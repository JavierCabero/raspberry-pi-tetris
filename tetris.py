
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


def main():
    
    running = True

    global moving_piece
    moving_piece = Triangle()
    moving_piece.draw()

    # main loop
    while running:
    
        # process input
        if moving_piece != None: moving_piece.keyboard_input()

    clock.tick(30)                                            
if __name__ == '__main__':
    main()