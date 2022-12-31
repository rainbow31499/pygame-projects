import pygame
from pygame.locals import *
import random
import time

start_time = None
end_time = None
active_bubble = None
bubble_positions = []
first_bubble = 1
game_running = False
remaining_time = 0
elapsed_time = 0
show_menu = True
options =  [{'name': 'Timed mode', 'pos': 150},
            {'name': 'Pop 100 bubbles', 'pos': 200},
            {'name': 'Escape the devil', 'pos': 250}]
mode = None
active_option = None
devil_position = 0
bubble_pops = []

def start():
    global bubble_positions, first_bubble, start_time, end_time, game_running, remaining_time, elapsed_time, show_menu, devil_position
    show_menu = False
    game_running = True
    bubble_positions = []
    first_bubble = 1
    for i in range(100):
        bubble_positions.append((random.randint(50,450),random.randint(50,450)))

    start_time = time.time()
    if mode == 0:
        end_time = time.time() + 60
        remaining_time = 60
    elif mode == 1:
        elapsed_time = 0
    elif mode == 2:
        devil_position = 0
        end_time = time.time() + 5
        remaining_time = 5


running = True
screen = pygame.display.set_mode([500,500])

pygame.init()
font = pygame.font.Font(None, 32)

while running == True:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if active_bubble == 0 and game_running:
                bubble_pop_time = time.time()
                bubble_pop_pos = bubble_positions[0]
                bubble_pops.append((bubble_pop_time, bubble_pop_pos))
                del bubble_positions[0]
                if mode == 0 or mode == 2:
                    bubble_positions.append((random.randint(50,450),random.randint(50,450)))
                first_bubble += 1
            
            if show_menu:
                if active_option != None:
                    mode = active_option
                    start()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and game_running == False:
                show_menu = True
                #start()

    mouse_pos = pygame.mouse.get_pos()

    number_of_bubbles = len(bubble_positions)
    
    active_bubble = None
    if game_running:
        for i in range(number_of_bubbles):
            if (bubble_positions[i][0] - mouse_pos[0])**2 + (bubble_positions[i][1] - mouse_pos[1])**2 <= 20**2:
                active_bubble = i
                break
    
    if game_running:
        if mode == 0:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                game_running = False
        elif mode == 1:
            elapsed_time = time.time() - start_time
            if bubble_positions == []:
                game_running = False
        elif mode == 2:
            remaining_time = end_time - time.time()
            if remaining_time <= 0:
                devil_position += 1
                end_time = time.time() + (4 * 0.97**(devil_position-1) + 1)
                remaining_time = 4 * 0.97**(devil_position-1) + 1
            if devil_position >= first_bubble:
                game_running = False

    for i in range(len(bubble_pops)):
        if time.time() > bubble_pops[i][0] + 0.5:
            del bubble_pops[i]
            break

    if show_menu:
        if 100 <= mouse_pos[0] <= 400:
            for option in range(len(options)):
                if options[option]['pos'] <= mouse_pos[1] <= options[option]['pos'] + 30:
                    active_option = option
                    break
            else:
                active_option = None
        else:
            active_option = None
    
    
    screen.fill((255,255,255))
    
    for i in range(number_of_bubbles):
        if active_bubble == number_of_bubbles-(i+1):
            pygame.draw.circle(screen, (128,128,128), bubble_positions[-(i+1)], 20, 0)
        else:
            pygame.draw.circle(screen, (255,255,255), bubble_positions[-(i+1)], 20, 0)
        
        pygame.draw.circle(screen, (0,0,0), bubble_positions[-(i+1)], 20, 1)
        number = font.render(str(first_bubble + number_of_bubbles - 1 - i), True, (0,0,0))
        screen.blit(number, (bubble_positions[-(i+1)][0] - number.get_size()[0]/2, bubble_positions[-(i+1)][1] - number.get_size()[1]/2))

    for bubble_pop in bubble_pops:
        for x0,y0,x1,y1 in [(20,0,25,0),
                            (-20,0,-25,0),
                            (0,20,0,25),
                            (0,-20,0,-25),
                            (14,14,18,18),
                            (14,-14,18,-18),
                            (-14,14,-18,18),
                            (-14,-14,-18,-18)]:
            pygame.draw.line(screen, (128,192,255), (bubble_pop[1][0]+x0,bubble_pop[1][1]+y0), (bubble_pop[1][0]+x1,bubble_pop[1][1]+y1))

    if show_menu == True:
        for i in range(len(options)):
            option = options[i]
            if active_option == i:
                pygame.draw.rect(screen, (128,128,128), Rect(100,option['pos'],300,30), 0)
            else:
                pygame.draw.rect(screen, (255,255,255), Rect(100,option['pos'],300,30), 0)
            pygame.draw.rect(screen, (0,0,0), Rect(100,option['pos'],300,30), 1)
            text = font.render(option['name'], True, (0,0,0))
            screen.blit(text, (250 - text.get_size()[0]/2,option['pos']+5))

    if mode == 0:
        if remaining_time >= 0:
            time_text = font.render('{0:.1f}'.format(remaining_time), True, (0,0,0))
        else:
            time_text = font.render('Time\'s up! Your score: {}'.format(first_bubble-1), True, (0,0,0))
        screen.blit(time_text, (10,10))
    elif mode == 1:
        if len(bubble_positions) > 0:
            time_text = font.render('{:.1f}'.format(elapsed_time), True, (0,0,0))
        else:
            time_text = font.render('You completed the game in {:.1f} seconds'.format(elapsed_time), True, (0,0,0))
        screen.blit(time_text, (10,10))
    elif mode == 2:
        if game_running:
            time_text = font.render('Devil will move to position {} in {:.1f} seconds'.format(devil_position+1, remaining_time), True, (0,0,0))
        else:
            time_text = font.render('Game over! Your score: {}'.format(first_bubble-1), True, (0,0,0))
        screen.blit(time_text, (10,10))

    pygame.display.flip()

pygame.quit()