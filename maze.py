# Import packages

import random
import pygame
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

# Set initial conditions

length = 60
height = 40
start = (0,0)
end = (length-1,height-1)

# Helper functions for moving

def left(pos):
    return (pos[0]-1, pos[1])

def right(pos):
    return (pos[0]+1, pos[1])

def up(pos):
    return (pos[0], pos[1]-1)

def down(pos):
    return (pos[0], pos[1]+1)

# Helper function for testing valid position

def ingrid(pos):
    cond1 = (0 <= pos[0] < length)
    cond2 = (0 <= pos[1] < height)
    return (cond1 and cond2)

# Generate the maze

def complete(visited):
    for x in range(length):
        for y in range(height):
            if (x,y) not in visited:
                return False
    
    return True

generate_prob = 0.8
branching_prob = 0.1

def generate_maze():
    maze = {}
    
    for x in range(length):
        for y in range(height):
            maze[(x,y)] = []
    
    visited = [start]
    
    while complete(visited) == False:
        for pos in visited:
            if pos == end:
                pass
            
            elif maze[pos] == []:
                if random.random() <= generate_prob:
                    direction = random.randint(0,3)
                    if direction == 0:
                        if ingrid(left(pos)) and (left(pos) not in visited):
                            maze[pos].append('L')
                            visited.append(left(pos))
                            
                    elif direction == 1:
                        if ingrid(right(pos)) and (right(pos) not in visited):
                            maze[pos].append('R')
                            visited.append(right(pos))
                            
                    elif direction == 2:
                        if ingrid(up(pos)) and (up(pos) not in visited):
                            maze[pos].append('U')
                            visited.append(up(pos))
                            
                    elif direction == 3:
                        if ingrid(down(pos)) and (down(pos) not in visited):
                            maze[pos].append('D')
                            visited.append(down(pos))
                            
            elif maze[pos] != []:
                if random.random() <= branching_prob and pos != start:
                    direction = random.randint(0,3)
                    if direction == 0:
                        if ingrid(left(pos)) and (left(pos) not in visited):
                            maze[pos].append('L')
                            visited.append(left(pos))
                            
                    elif direction == 1:
                        if ingrid(right(pos)) and (right(pos) not in visited):
                            maze[pos].append('R')
                            visited.append(right(pos))
                            
                    elif direction == 2:
                        if ingrid(up(pos)) and (up(pos) not in visited):
                            maze[pos].append('U')
                            visited.append(up(pos))
                            
                    elif direction == 3:
                        if ingrid(down(pos)) and (down(pos) not in visited):
                            maze[pos].append('D')
                            visited.append(down(pos))
                            
    return maze
                
# Helper functions to test for walls

def hor_wall(maze, pos):
    # Test for a horizontal wall between pos and up(pos)
    cond1 = ('U' in maze[pos])
    cond2 = ('D' in maze[up(pos)])
    return (not (cond1 or cond2))

def ver_wall(maze, pos):
    # Test for a vertical wall between pos and left(pos)
    cond1 = ('L' in maze[pos])
    cond2 = ('R' in maze[left(pos)])
    return (not (cond1 or cond2))

# Generate the maze

# Set screen parameters

square_length = 20
margin_width = 10

screen_length = length * square_length + 2 * margin_width
screen_height = height * square_length + 2 * margin_width

# Initialize Pygame

pygame.init()

screen = pygame.display.set_mode([screen_length, screen_height])

current_pos = start

success = False

running = True

maze = generate_maze()

fontsys24 = pygame.font.SysFont(None, 48)

while running:

    screen.fill((255, 255, 255))
    
    # Draw borders of maze

    pygame.draw.line(screen, (0,0,0), [margin_width, margin_width], [screen_length - margin_width, margin_width], width = 2)
    pygame.draw.line(screen, (0,0,0), [margin_width, margin_width], [margin_width, screen_height - margin_width], width = 2)
    pygame.draw.line(screen, (0,0,0), [margin_width, screen_height - margin_width], [screen_length - margin_width, screen_height - margin_width], width = 2)
    pygame.draw.line(screen, (0,0,0), [screen_length - margin_width, margin_width], [screen_length - margin_width, screen_height - margin_width], width = 2)
    
    # Draw walls where they exist
    
    for x in range(length):
        for y in range(1, height):
            if hor_wall(maze, (x,y)):
                pygame.draw.line(screen, (0,0,0), [margin_width + x * square_length, margin_width + y * square_length], [margin_width + (x+1) * square_length, margin_width + y * square_length])
                
    for x in range(1, length):
        for y in range(height):
            if ver_wall(maze, (x,y)):
                pygame.draw.line(screen, (0,0,0), [margin_width + x * square_length, margin_width + y * square_length], [margin_width + x * square_length, margin_width + (y+1) * square_length])
                
    # Indicate starting (green) and ending (red) positions
    
    pygame.draw.circle(screen, (0,255,0), [margin_width + (start[0] + 1/2) * square_length, margin_width + (start[1] + 1/2) * square_length], square_length * 1/4)
    
    pygame.draw.circle(screen, (255,0,0), [margin_width + (end[0] + 1/2) * square_length, margin_width + (end[1] + 1/2) * square_length], square_length * 1/4)

    # Run events
    
    if current_pos == end:
        success = True
    
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(margin_width + (current_pos[0] + 1/4) * square_length, margin_width + (current_pos[1] + 1/4) * square_length, 1/2 * square_length, 1/2 * square_length))
    
    if success == True:
        message_width = 70
        message_height = 70
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(screen_length / 2 - message_width, screen_height / 2 - message_height, message_width * 2, message_height * 2))
        pygame.draw.line(screen, (0,0,0), [screen_length / 2 - message_width, screen_height / 2 - message_height], [screen_length / 2 + message_width, screen_height / 2 - message_height])
        pygame.draw.line(screen, (0,0,0), [screen_length / 2 - message_width, screen_height / 2 - message_height], [screen_length / 2 - message_width, screen_height / 2 + message_height])
        pygame.draw.line(screen, (0,0,0), [screen_length / 2 - message_width, screen_height / 2 + message_height], [screen_length / 2 + message_width, screen_height / 2 + message_height])
        pygame.draw.line(screen, (0,0,0), [screen_length / 2 + message_width, screen_height / 2 - message_height], [screen_length / 2 + message_width, screen_height / 2 + message_height])
        pygame.draw.polygon(screen, (255,216,0),
            [[screen_length / 2 + 50 * 0, screen_height / 2 + 50 * -1],
             [screen_length / 2 + 50 * 0.224514, screen_height / 2 + 50 * -0.309017],
             [screen_length / 2 + 50 * 0.951057, screen_height / 2 + 50 * -0.309017],
             [screen_length / 2 + 50 * 0.363271, screen_height / 2 + 50 * 0.118034],
             [screen_length / 2 + 50 * 0.587785, screen_height / 2 + 50 * 0.809017],
             [screen_length / 2 + 50 * 0, screen_height / 2 + 50 * 0.381966],
             [screen_length / 2 + 50 * -0.587785, screen_height / 2 + 50 * 0.809017],
             [screen_length / 2 + 50 * -0.363271, screen_height / 2 + 50 * 0.118034],
             [screen_length / 2 + 50 * -0.951057, screen_height / 2 + 50 * -0.309017],
             [screen_length / 2 + 50 * -0.224514, screen_height / 2 + 50 * -0.309017]])
        success_text = fontsys24.render('Success', True, (0,0,0))
        screen.blit(success_text, [screen_length / 2 - 70, screen_height / 2 - 20])
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if success == False:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if ingrid(up(current_pos)):
                        if hor_wall(maze, current_pos) == False:
                            current_pos = up(current_pos)
                            
                elif event.key == K_DOWN:
                    if ingrid(down(current_pos)):
                        if hor_wall(maze, down(current_pos)) == False:
                            current_pos = down(current_pos)
                            
                elif event.key == K_LEFT:
                    if ingrid(left(current_pos)):
                        if ver_wall(maze, current_pos) == False:
                            current_pos = left(current_pos)
                            
                elif event.key == K_RIGHT:
                    if ingrid(right(current_pos)):
                        if ver_wall(maze, right(current_pos)) == False:
                            current_pos = right(current_pos)
                            
        elif success == True:
            if event.type == KEYDOWN:
                maze = generate_maze()
                current_pos = start
                success = False
                    
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                
        if event.type == pygame.QUIT:
            running = False

# End program

pygame.quit()