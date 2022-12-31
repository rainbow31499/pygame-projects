import pygame # Of course we need to import Pygame!
from pygame.locals import * # Stuff like keyboard keys to make easier to access

# Initialize variables

# Initialize the Pygame interface
running = True

pygame.init()

screen = pygame.display.set_mode([500,500])

while running == True:
    # BACKEND - internal variables, updates

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        # Add other controls here

        if event.type == KEYDOWN:
            pass # add if event.key == ...: to implement certain controls when pressing a keyboard key

        if event.type == MOUSEBUTTONDOWN:
            pass # When pressing the mouse click

        if event.type == MOUSEBUTTONUP:
            pass # When releasing the mouse click

    # FRONTEND - Display the screen based on the variables
    screen.fill((255,255,255))

    pygame.display.flip()

pygame.quit()