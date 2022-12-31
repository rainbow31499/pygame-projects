# Version 0.1: Create a falling 1x1 block upon pressing SPACE

import pygame
from pygame.locals import *
import time
import random

class Block:
    def __init__(self, blocks, center_of_rotation):
        self.blocks = blocks
        self.center_of_rotation = center_of_rotation
        # center_of_rotation = True means block's center of rotation is center of (0,0) position
        # center_of_rotation = False means block's center of rotation is bottom left of (0,0) position
        
    def rotate(self): # clockwise 90 deg
        for block in self.blocks:
            if self.center_of_rotation == True:
                new_block = [block[1], -block[0]]
            elif self.center_of_rotation == False:
                new_block = [block[1], -block[0]-1]

pygame.init()

screen = pygame.display.set_mode(size = [350,650])

running = True

game_running = False

active_block = None

while running:
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,0,0), True, [(25,25),(325,25),(325,625),(25,625)])
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            if game_running == False:
                game_running = True
                active_block = Block(blocks=[[0,0]], center_of_rotation=True)
                active_block_position = [5,20] # location of (0,0) block
                block_fall_time = time.time()
            
    if game_running == True:
        if time.time() - block_fall_time >= 0.5:
            fallable = True
            for block in active_block.blocks:
                if block[1] + active_block_position[1] - 1 < 0:
                    fallable = False
            if fallable == True:
                active_block_position[1] -= 1
                block_fall_time = time.time()
    
    if active_block != None:
        for block in active_block.blocks:
            block_position = [block[0]+active_block_position[0], block[1]+active_block_position[1]]
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(27+30*(block_position[0]),597-30*(block_position[1]),26,26))
            
    pygame.display.flip()
    
pygame.quit()