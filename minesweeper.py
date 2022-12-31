import pygame
from pygame.locals import *
import random
import time

class MinesweeperBoard:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines_no = mines
        self.mines = [[False for x in range(width)] for y in range(height)]
        self.opened = [[False for x in range(width)] for y in range(height)]
        self.flags = [[False for x in range(width)] for y in range(height)]
        self.clues = [[0 for x in range(width)] for y in range(height)]
        self.mines_rem = self.mines_no
        self.running = False
        self.start_time = None
        self.total_time = 0
        self.game_complete = False
        self.success = False
                
    def square_value(self, pos):
        if self.mines[pos[1]][pos[0]] == True:
            return 'X'
        else:
            mines_in_neighbourhood = 0
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if 0 <= pos[0]+x < self.width and 0 <= pos[1]+y < self.height:
                        mines_in_neighbourhood += self.mines[pos[1]+y][pos[0]+x]
            return mines_in_neighbourhood
    
    def assemble_clues(self):
        clues = [[self.square_value((x,y)) for x in range(self.width)] for y in range(self.height)]
        self.clues = clues
    
    def completed(self):
        complete = True
        for x in range(self.width):
            for y in range(self.height):
                if self.mines[y][x] == False and self.opened[y][x] == False:
                    complete = False
        return complete
    
    def open_square(self, pos):
        if self.opened[pos[1]][pos[0]] == False and self.flags[pos[1]][pos[0]] == False:
            if self.running == False and self.game_complete == False:
                self.running = True
                self.start_time = time.time()
                while sum([sum(row) for row in self.mines]) < self.mines_no:
                    random_pos = (random.randint(0,self.width-1),random.randint(0,self.height-1))
                    if self.mines[random_pos[1]][random_pos[0]] == False and (random_pos[0] != pos[0] or random_pos[1] != pos[1]):
                        self.mines[random_pos[1]][random_pos[0]] = True
                    else:
                        continue
                self.assemble_clues()
            if self.running == True:
                self.opened[pos[1]][pos[0]] = True
                if self.clues[pos[1]][pos[0]] == 0:
                    for x in [-1,0,1]:
                        for y in [-1,0,1]:
                            if (x != 0 or y != 0) and 0 <= pos[0]+x < self.width and 0 <= pos[1]+y < self.height:
                                self.open_square((pos[0]+x,pos[1]+y))
                elif self.clues[pos[1]][pos[0]] == 'X':
                    self.game_complete = True
                    self.total_time = int(time.time() - self.start_time)
                    for x in range(self.width):
                        for y in range(self.height):
                            if self.mines[y][x] == True:
                                self.opened[y][x] = True
                            
        if self.completed() == True:
            self.success = True
            self.game_complete = True
            self.total_time = int(time.time() - self.start_time)

    def add_flag(self, pos):
        self.flags[pos[1]][pos[0]] = not self.flags[pos[1]][pos[0]]
        self.mines_rem += (-1)**board.flags[pos[1]][pos[0]]

    def reset(self):
        self.mines = [[False for x in range(width)] for y in range(height)]
        self.opened = [[False for x in range(width)] for y in range(height)]
        self.flags = [[False for x in range(width)] for y in range(height)]
        self.clues = [[0 for x in range(width)] for y in range(height)]
        self.mines_rem = self.mines_no
        self.running = False
        self.start_time = None
        self.total_time = 0
        self.game_complete = False
        self.success = False

board_size = [16,16]
total_mines = 40

board = MinesweeperBoard(board_size[0],board_size[1],total_mines)

width = 20 + board_size[0] * 20
height = 50 + board_size[1] * 20

number_colors = \
    {1: (0,0,255),
     2: (0,128,0),
     3: (255,0,0),
     4: (0,0,128),
     5: (128,0,0),
     6: (0,128,128),
     7: (0,0,0),
     8: (128,128,128)}

pygame.init()

screen = pygame.display.set_mode([width, height])

text_font_24 = pygame.font.SysFont(None,24)
text_font_36 = pygame.font.SysFont(None,36)

running = True

while running == True:
    screen.fill((255,255,255))
    
    for x in range(board_size[0]):
        for y in range(board_size[1]):
            if board.opened[y][x] == False:
                if 10+20*x < pygame.mouse.get_pos()[0] < 30+20*x and 40+20*y < pygame.mouse.get_pos()[1] < 60+20*y:
                    pygame.draw.rect(screen,(192,192,192),Rect(10+20*x,40+20*y,20,20))
                else:
                    pygame.draw.rect(screen,(228,228,228),Rect(10+20*x,40+20*y,20,20))
                if board.flags[y][x] == True:
                    screen.blit(text_font_24.render('F',True,(255,0,0)),(16+20*x,43+20*y))
            else:
                if board.clues[y][x] == 'X':
                    pygame.draw.rect(screen,(255,0,0),Rect(10+20*x,40+20*y,20,20))
                    screen.blit(text_font_24.render('X',True,(0,0,0)),(16+20*x,43+20*y))
                elif board.clues[y][x] != 0:
                    clue = board.clues[y][x]
                    screen.blit(text_font_24.render(str(clue),True,number_colors[clue]),(16+20*x,43+20*y))
    
    for x in range(board_size[0]+1):
        pygame.draw.line(screen,(0,0,0),(10+20*x,40),(10+20*x,40+20*board_size[1]))
        
    for y in range(board_size[1]+1):
        pygame.draw.line(screen,(0,0,0),(10,40+20*y),(10+20*board_size[0],40+20*y))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 and board.game_complete == False:
            for x in range(board_size[0]):
                for y in range(board_size[1]):
                    if 10+20*x < event.pos[0] < 30+20*x and 40+20*y < event.pos[1] < 60+20*y:
                        board.open_square((x,y))
        elif event.type == MOUSEBUTTONDOWN and event.button == 3 and board.game_complete == False:
            for x in range(board_size[0]):
                for y in range(board_size[1]):
                    if 10+20*x < event.pos[0] < 30+20*x and 40+20*y < event.pos[1] < 60+20*y and board.opened[y][x] == False:
                        board.add_flag((x,y))
        elif event.type == KEYDOWN and event.key == K_SPACE:
            board.reset()
    
    if board.game_complete == False and board.running == False:
        total_time = 0
    elif board.game_complete == False and board.running == True:
        total_time = int(time.time() - board.start_time)
    elif board.game_complete == True:
        total_time = board.total_time
        if board.success == True:
            screen.blit(text_font_36.render('Success!',True,(0,255,0)),(width/2-50,10))
        elif board.success == False:
            screen.blit(text_font_36.render('Game Over',True,(255,0,0)),(width/2-50,10))
        
    screen.blit(text_font_36.render(str(total_time),True,(0,0,0)),(30,10))
    screen.blit(text_font_36.render(str(board.mines_rem),True,(0,0,0)),(width-40,10))
    
    pygame.display.flip()
    
pygame.quit()