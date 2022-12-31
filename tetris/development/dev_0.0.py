# Version 0.0: Start by creating the initial 10x20 board

import pygame
from pygame.locals import *
import time
import random

pygame.init()

screen = pygame.display.set_mode(size = [350,650])

running = True

while running:
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,0,0), True, [(25,25),(325,25),(325,625),(25,625)])
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
    pygame.display.flip()
    
pygame.quit()