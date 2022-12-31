import pygame

from pygame.locals import *

pygame.init()

length = 1000
height = 500

screen = pygame.display.set_mode([length, height])

running = True

font = pygame.font.SysFont(None, 48)
smallfont = pygame.font.SysFont(None, 24)

text = ''

pos = 'None'
pos_lclick_down = 'None'
pos_lclick_up = 'None'
pos_rclick_down = 'None'
pos_rclick_up = 'None'

clicked = False
unclicked = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        elif event.type == KEYDOWN:
            text = str(event.key)
        
        elif event.type == MOUSEBUTTONDOWN:
            clicked = not clicked
            if event.button == 1:
                pos_lclick_down = str(event.pos)
            elif event.button == 3:
                pos_rclick_down = str(event.pos)
                
        elif event.type == MOUSEBUTTONUP:
            unclicked = not unclicked
            if event.button == 1:
                pos_lclick_up = str(event.pos)
            elif event.button == 3:
                pos_rclick_up = str(event.pos)
            
    screen.fill((255,255,255))
    
    pos = str(pygame.mouse.get_pos())
    
    img1 = font.render(text, True, (0,0,0))
    img2 = font.render(pos, True, (0,0,0))
    img3 = font.render(pos_lclick_down, True, (255,0,0))
    img4 = font.render(pos_rclick_down, True, (0,0,255))
    img5 = font.render(pos_lclick_up, True, (255,0,0))
    img6 = font.render(pos_rclick_up, True, (0,0,255))
    
    screen.blit(img1, (0,0))
    screen.blit(img2, (0,30))
    screen.blit(img3, (0,100))
    screen.blit(img4, (300,100))
    screen.blit(img5, (0,70))
    screen.blit(img6, (300,70))
    
    if clicked == True:
        screen.blit(font.render('You clicked', True, (0,0,0)), (0,200))
        
    if unclicked == True:
        screen.blit(font.render('You unclicked', True, (0,0,0)), (0,230))
        
    if pygame.mouse.get_pressed()[0] == True:
        screen.blit(font.render('You are clicking left', True, (0,0,0)), (300,200))
        
    if pygame.mouse.get_pressed()[2] == True:
        screen.blit(font.render('You are clicking right', True, (0,0,0)), (300,230))
        
    keyboard_positions = \
    {K_q: (30,300),
     K_w: (60,300),
     K_e: (90,300),
     K_r: (120,300),
     K_t: (150,300),
     K_y: (180,300),
     K_u: (210,300),
     K_i: (240,300),
     K_o: (270,300),
     K_p: (300,300),
     K_a: (40,350),
     K_s: (70,350),
     K_d: (100,350),
     K_f: (130,350),
     K_g: (160,350),
     K_h: (190,350),
     K_j: (220,350),
     K_k: (250,350),
     K_l: (280,350),
     K_z: (60,400),
     K_x: (90,400),
     K_c: (120,400),
     K_v: (150,400),
     K_b: (180,400),
     K_n: (210,400),
     K_m: (240,400)}
        
    for key in keyboard_positions:
        if pygame.key.get_pressed()[key] == True:
            screen.blit(font.render(chr(key).upper(), True, (255,0,0)), keyboard_positions[key])
        else:
            screen.blit(font.render(chr(key).upper(), True, (0,0,0)), keyboard_positions[key])
            
    if pygame.key.get_pressed()[K_SPACE] == True:
        screen.blit(font.render('SPACE', True, (255,0,0)),(150,450))
    else:
        screen.blit(font.render('SPACE', True, (0,0,0)),(150,450))
    
    pygame.display.flip()
    
pygame.quit()