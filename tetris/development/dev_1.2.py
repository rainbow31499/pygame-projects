# Version 1.2: Put "next block" on the screen

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
    
    def rotatable(self, position, dropped_blocks):
        dropped_blocks_pos = [block[0] for block in dropped_blocks]
        rotated_block = self.rotation()
        result = True
        for block in rotated_block:
            block_position = [block[0] + position[0], block[1] + position[1]]
            if block_position[1] < 0 or block_position[0] < 0 or block_position[0] > 9 or block_position in dropped_blocks_pos:
                result = False
        return result
    
    def rotate(self):
        self.blocks = self.rotation()
                
    def fallable(self, position, dropped_blocks):
        dropped_blocks_pos = [block[0] for block in dropped_blocks]
        result = True
        for block in self.blocks:
            block_moved = [block[0] + position[0], block[1] + position[1] - 1]
            if block_moved[1] < 0 or block_moved in dropped_blocks_pos:
                result = False
        return result
    
    def leftable(self, position, dropped_blocks):
        dropped_blocks_pos = [block[0] for block in dropped_blocks]
        result = True
        for block in self.blocks:
            block_moved = [block[0] + position[0] - 1, block[1] + position[1]]
            if block_moved[0] < 0 or block_moved in dropped_blocks_pos:
                result = False
        return result
    
    def rightable(self, position, dropped_blocks):
        dropped_blocks_pos = [block[0] for block in dropped_blocks]
        result = True
        for block in self.blocks:
            block_moved = [block[0] + position[0] + 1, block[1] + position[1]]
            if block_moved[0] > 9 or block_moved in dropped_blocks_pos:
                result = False
        return result

tetris_blocks = [[[[-2,-1],[-1,-1],[0,-1],[1,-1]],False],
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

pygame.init()

screen = pygame.display.set_mode(size = [350,800])

running = True

dropped_blocks = []

game_running = False
game_over = False

block_number = None
next_block = random.randint(0,6)
active_block = None
active_block_position = [5,21]
block_fall_time = None
speed = 2
fall_speed = None

level = 1
score = 0
combo = 0
high_score = int(open("high_score.txt", "rt").read())

lines_to_clear = 10
level_lines = 10

while running:
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,0,0), True, [(25,175),(325,175),(325,775),(25,775)])
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_running == False:
                    game_running = True
                    game_over = False
                    level = 1
                    score = 0
                    combo = 0
                    speed = 2
                    dropped_blocks = []
                    block_number = next_block
                    active_block = Block(blocks=tetris_blocks[block_number][0], center_of_rotation=tetris_blocks[block_number][1])
                    next_block = random.randint(0,6)
                    active_block_position = [5,21] # location of (0,0) block
                    block_fall_time = time.time()
                    fall_speed = speed
            elif event.key == K_LEFT:
                if active_block.leftable(active_block_position, dropped_blocks) == True:
                    active_block_position[0] -= 1
            elif event.key == K_RIGHT:
                if active_block.rightable(active_block_position, dropped_blocks) == True:
                    active_block_position[0] += 1
            elif event.key == K_DOWN:
                fall_speed = 100
            elif event.key == K_UP:
                if active_block.rotatable(active_block_position, dropped_blocks) == True:
                    active_block.rotate()
    
    for block in dropped_blocks:
        if block[0][1] >= 20:
            game_running = False
            game_over = True
    
    if game_running == True:
        if time.time() - block_fall_time >= 1/fall_speed:
            if active_block.fallable(active_block_position, dropped_blocks) == True:
                active_block_position[1] -= 1
                block_fall_time = time.time()
            else:
                for block in active_block.blocks:
                    block_position = [block[0]+active_block_position[0], block[1]+active_block_position[1]]
                    dropped_blocks.append([block_position, tetris_colors[block_number]])
                
                block_number = next_block
                active_block = Block(blocks=tetris_blocks[block_number][0], center_of_rotation=tetris_blocks[block_number][1])
                next_block = random.randint(0,6)
                active_block_position = [5,21]
                block_fall_time = time.time()
                fall_speed = speed
                
                lines_cleared = 0
                for row in range(20):
                    dropped_blocks_pos = [block[0] for block in dropped_blocks]
                    row_complete = True
                    for col in range(10):
                        if [col,19-row] not in dropped_blocks_pos:
                            row_complete = False
                    
                    if row_complete == True:
                        lines_cleared += 1
                        blocks_to_remove = []
                        for block in dropped_blocks:
                            if block[0][1] == 19-row:
                                blocks_to_remove.append(block)
                        for block in blocks_to_remove:
                            dropped_blocks.remove(block)
                        for block in dropped_blocks:
                            if block[0][1] > 19-row:
                                block[0][1] -= 1

                lines_to_clear -= lines_cleared

                level_score = 10 + (level-1) * 2

                multiplier = 0
                for line in range(lines_cleared):
                    multiplier += line + 1
                score += multiplier * (level_score + 5 * combo)
                if score > high_score:
                    high_score = score

                if lines_cleared >= 1:
                    combo += 1
                else:
                    combo = 0

                while lines_to_clear <= 0:
                    level += 1
                    lines_to_clear += (20 + (level-1) * 2)
                    level_lines = (20 + (level-1) * 2)

                speed = 2 + 0.2 * (level-1)
    
    if active_block != None:
        for block in active_block.blocks:
            block_position = [block[0]+active_block_position[0], block[1]+active_block_position[1]]
            pygame.draw.rect(screen, tetris_colors[block_number], pygame.Rect(27+30*(block_position[0]),747-30*(block_position[1]),26,26))
            
    for block in dropped_blocks:
        pygame.draw.rect(screen, block[1], pygame.Rect(27+30*(block[0][0]),747-30*(block[0][1]),26,26))

    font36 = pygame.font.Font(None, 36)
    level_text = font36.render("LEVEL " + str(level), True, (0,0,0))
    screen.blit(level_text, (25,15))
    score_text = font36.render("SCORE " + str(score), True, (0,0,0))
    screen.blit(score_text, (25,45))
    score_text = font36.render("HIGH SCORE " + str(high_score), True, (0,0,0))
    screen.blit(score_text, (25,75))

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(15,155,320,5))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(16,156,318*(1-lines_to_clear/level_lines),3))

    if combo >= 2:
        score_text = font36.render("COMBO " + str(combo), True, (255,0,0))
        screen.blit(score_text, (200,15))

    pygame.draw.lines(screen, (0,0,0), True, [(250,65),(340,65),(340,145),(250,145)])
    font24 = pygame.font.Font(None, 24)
    next_text = font24.render("NEXT", True, (0,0,0))
    screen.blit(next_text, (275,75))
    for block in tetris_blocks[next_block][0]:
        pygame.draw.rect(screen, tetris_colors[next_block], pygame.Rect(300-10*tetris_blocks[next_block][1]+20*(block[0]),100+20*tetris_blocks[next_block][1]-20*(block[1]),17,17))

    if game_over == True:
        game_over_text = font36.render("GAME OVER", True, (0,0,0))
        screen.blit(game_over_text, (25,105))
            
    pygame.display.flip()
    
pygame.quit()

with open("high_score.txt", "wt") as f:
    f.write(str(high_score))