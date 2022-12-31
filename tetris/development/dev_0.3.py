# Version 0.3: Add the seven Tetris blocks and spawn random blocks to drop

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
        
    def rotation(self): # clockwise 90 deg
        old_blocks = list(self.blocks)
        new_blocks = []
        for block in old_blocks:
            if self.center_of_rotation == True:
                new_block = [block[1], -block[0]]
            elif self.center_of_rotation == False:
                new_block = [block[1], -block[0]-1]
            new_blocks.append(new_block)
        return new_blocks
    
    def rotatable(self, position):
        rotated_block = self.rotation()
        result = True
        for block in rotated_block:
            if block[1] + position[1] < 0 or block[0] + position[0] < 0 or block[0] + position[0] > 9:
                result = False
        return result
    
    def rotate(self):
        self.blocks = self.rotation()
                
    def fallable(self, position):
        result = True
        for block in self.blocks:
            if block[1] + position[1] - 1 < 0:
                result = False
        return result
    
    def leftable(self, position):
        result = True
        for block in self.blocks:
            if block[0] + position[0] - 1 < 0:
                result = False
        return result
    
    def rightable(self, position):
        result = True
        for block in self.blocks:
            if block[0] + position[0] + 1 > 9:
                result = False
        return result

pygame.init()

screen = pygame.display.set_mode(size = [350,650])

running = True

game_running = False

tetris_blocks = [[[[-2,0],[-1,0],[0,0],[1,0]],False],
                 [[[-1,1],[-1,0],[0,0],[1,0]],True],
                 [[[-1,0],[0,0],[1,0],[1,1]],True],
                 [[[0,0],[-1,0],[0,-1],[-1,-1]],False],
                 [[[-1,0],[0,0],[0,1],[1,1]],True],
                 [[[-1,0],[0,0],[0,1],[1,0]],True],
                 [[[-1,1],[0,1],[0,0],[1,0]],True]]

tetris_colors = [(0,255,255),
                 (0,0,255),
                 (255,128,0),
                 (255,255,0),
                 (0,255,0),
                 (128,0,255),
                 (255,0,0)]

active_block = None
active_block_position = [5,20]
fall_period = 0.5

while running:
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,0,0), True, [(25,25),(325,25),(325,625),(25,625)])
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_running == False:
                    game_running = True
                    block_number = random.randint(0,6)
                    active_block = Block(blocks=tetris_blocks[block_number][0], center_of_rotation=tetris_blocks[block_number][1])
                    active_block_position = [5,20] # location of (0,0) block
                    block_fall_time = time.time()
                    fall_period = 0.5
            elif event.key == K_LEFT:
                if active_block.leftable(active_block_position) == True:
                    active_block_position[0] -= 1
            elif event.key == K_RIGHT:
                if active_block.rightable(active_block_position) == True:
                    active_block_position[0] += 1
            elif event.key == K_DOWN:
                fall_period = 0.01
            elif event.key == K_UP:
                if active_block.rotatable(active_block_position) == True:
                    active_block.rotate()
                
            
    if game_running == True:
        if time.time() - block_fall_time >= fall_period:
            if active_block.fallable(active_block_position) == True:
                active_block_position[1] -= 1
                block_fall_time = time.time()
            else:
                block_number = random.randint(0,6)
                active_block = Block(blocks=tetris_blocks[block_number][0], center_of_rotation=tetris_blocks[block_number][1])
                active_block_position = [5,20]
                block_fall_time = time.time()
                fall_period = 0.5
    
    if active_block != None:
        for block in active_block.blocks:
            block_position = [block[0]+active_block_position[0], block[1]+active_block_position[1]]
            pygame.draw.rect(screen, tetris_colors[block_number], pygame.Rect(27+30*(block_position[0]),597-30*(block_position[1]),26,26))
            
    pygame.display.flip()
    
pygame.quit()