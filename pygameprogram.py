# Simple pygame program

# Import and initialize the pygame library
import pygame

from pygame.locals import (K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit

circle_center = [250,250]

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                circle_center[1] += 5
                pygame.display.flip()
            if event.key == K_UP:
                circle_center[1] -= 5
                pygame.display.flip()
            if event.key == K_LEFT:
                circle_center[0] -= 5
                pygame.display.flip()
            if event.key == K_RIGHT:
                circle_center[0] += 5
                pygame.display.flip()
                
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == QUIT:
            running = False
            
        pygame.draw.circle(screen, (0, 0, 255), circle_center, 75)
            
        pygame.display.flip()

# Done! Time to quit.
pygame.quit()