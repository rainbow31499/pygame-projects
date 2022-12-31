# Version 2.0: Add Game class for easier development and addition of features, added ability to pause and restart game
# Press P for pause and R for restart (you will be asked to confirm)

import pygame
from pygame.locals import *
import time
import random

class Tetromino:
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

class Game:
    def __init__(self):
        self.high_score = int(open("high_score.txt", "rt").read())
        self.reset()
        self.running = False

    def reset(self):
        self.running = True
        self.game_over = False
        self.paused = False
        self.restart_q = False
        self.level = 1
        self.score = 0
        self.combo = 0
        self.speed = 2
        self.dropped_blocks = []
        self.next_block = random.randint(0,6)
        self.block_number = random.randint(0,6)
        self.active_block = Tetromino(blocks=tetris_blocks[self.block_number][0], center_of_rotation=tetris_blocks[self.block_number][1])
        self.active_block_position = [5,21] # location of (0,0) block
        self.block_fall_time = time.time()
        self.fall_speed = self.speed
        self.lines_to_clear = 10
        self.level_lines = 10

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

game = Game()

pygame.init()

screen = pygame.display.set_mode(size = [350,800])

running = True

while running:
    # CONTROLS #
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game.running == False:
                    game.reset()
            elif event.key == K_LEFT:
                if game.active_block.leftable(game.active_block_position, game.dropped_blocks) == True:
                    game.active_block_position[0] -= 1
            elif event.key == K_RIGHT:
                if game.active_block.rightable(game.active_block_position, game.dropped_blocks) == True:
                    game.active_block_position[0] += 1
            elif event.key == K_DOWN:
                game.fall_speed = 100
            elif event.key == K_UP:
                if game.active_block.rotatable(game.active_block_position, game.dropped_blocks) == True:
                    game.active_block.rotate()
            elif event.key == K_p:
                game.paused = not(game.paused)
            elif event.key == K_r:
                if game.running == True:
                    game.restart_q = not(game.restart_q)

            if game.restart_q == True:
                if event.key == K_y:
                    game.restart_q = False
                    game.reset()
                elif event.key == K_n:
                    game.restart_q = False

    # COMPUTATION #
    for block in game.dropped_blocks:
        if block[0][1] >= 20:
            game.game_over = True
            game.running = False
    
    if game.running == True and game.paused == False:
        if time.time() - game.block_fall_time >= 1/game.fall_speed:
            if game.active_block.fallable(game.active_block_position, game.dropped_blocks) == True:
                game.active_block_position[1] -= 1
                game.block_fall_time = time.time()
            else:
                for block in game.active_block.blocks:
                    block_position = [block[0]+game.active_block_position[0], block[1]+game.active_block_position[1]]
                    game.dropped_blocks.append([block_position, tetris_colors[game.block_number]])
                
                game.block_number = game.next_block
                game.active_block = Tetromino(blocks=tetris_blocks[game.block_number][0], center_of_rotation=tetris_blocks[game.block_number][1])
                game.next_block = random.randint(0,6)
                game.active_block_position = [5,21]
                game.block_fall_time = time.time()
                game.fall_speed = game.speed
                
                lines_cleared = 0
                for row in range(20):
                    dropped_blocks_pos = [block[0] for block in game.dropped_blocks]
                    row_complete = True
                    for col in range(10):
                        if [col,19-row] not in dropped_blocks_pos:
                            row_complete = False
                    
                    if row_complete == True:
                        lines_cleared += 1
                        blocks_to_remove = []
                        for block in game.dropped_blocks:
                            if block[0][1] == 19-row:
                                blocks_to_remove.append(block)
                        for block in blocks_to_remove:
                            game.dropped_blocks.remove(block)
                        for block in game.dropped_blocks:
                            if block[0][1] > 19-row:
                                block[0][1] -= 1

                game.lines_to_clear -= lines_cleared

                level_score = 10 + (game.level-1) * 2

                multiplier = 0
                for line in range(lines_cleared):
                    multiplier += line + 1
                game.score += multiplier * (level_score + 5 * game.combo)
                if game.score > game.high_score:
                    game.high_score = game.score

                if lines_cleared >= 1:
                    game.combo += 1
                else:
                    game.combo = 0

                while game.lines_to_clear <= 0:
                    game.level += 1
                    game.lines_to_clear += (20 + (game.level-1) * 2)
                    game.level_lines = (20 + (game.level-1) * 2)

                game.speed = 2 + 0.2 * (game.level-1)
    
    # GAME DISPLAY #
    screen.fill((255,255,255))
    pygame.draw.lines(screen, (0,0,0), True, [(25,175),(325,175),(325,775),(25,775)])
    
    if game.active_block != None and game.running == True:
        for block in game.active_block.blocks:
            block_position = [block[0]+game.active_block_position[0], block[1]+game.active_block_position[1]]
            pygame.draw.rect(screen, tetris_colors[game.block_number], pygame.Rect(27+30*(block_position[0]),747-30*(block_position[1]),26,26))
            
    for block in game.dropped_blocks:
        pygame.draw.rect(screen, block[1], pygame.Rect(27+30*(block[0][0]),747-30*(block[0][1]),26,26))

    font36 = pygame.font.Font(None, 36)
    level_text = font36.render("LEVEL " + str(game.level), True, (0,0,0))
    screen.blit(level_text, (25,15))
    score_text = font36.render("SCORE " + str(game.score), True, (0,0,0))
    screen.blit(score_text, (25,45))
    score_text = font36.render("HIGH SCORE " + str(game.high_score), True, (0,0,0))
    screen.blit(score_text, (25,75))

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(15,155,320,5))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(16,156,318*(1-game.lines_to_clear/game.level_lines),3))

    if game.combo >= 2:
        score_text = font36.render("COMBO " + str(game.combo), True, (255,0,0))
        screen.blit(score_text, (200,15))

    pygame.draw.lines(screen, (0,0,0), True, [(250,65),(340,65),(340,145),(250,145)])
    font24 = pygame.font.Font(None, 24)
    next_text = font24.render("NEXT", True, (0,0,0))
    screen.blit(next_text, (275,75))
    for block in tetris_blocks[game.next_block][0]:
        pygame.draw.rect(screen, tetris_colors[game.next_block], pygame.Rect(300-10*tetris_blocks[game.next_block][1]+20*(block[0]),100+20*tetris_blocks[game.next_block][1]-20*(block[1]),17,17))

    if game.game_over == True:
        game_over_text = font36.render("GAME OVER", True, (0,0,0))
        screen.blit(game_over_text, (25,105))
    elif game.paused == True:
        paused_text = font36.render("PAUSED", True, (0,0,0))
        screen.blit(paused_text, (25,105))

    if game.restart_q == True:
        restart_text = font36.render("RESTART? Y N", True, (0,0,0))
        screen.blit(restart_text, (25,105))
            
    pygame.display.flip()
    
pygame.quit()

with open("high_score.txt", "wt") as f:
    f.write(str(game.high_score))