from graph import Graph
from character import Character
import user_interface
import map_points
import random
import pygame
from collections import deque
import os

########################################################################################################################
#                                                                                                                      #
# Maze Game                                                                                                            #
# Popa Daniel                                                                                                          #
# CEN 2.2B                                                                                                             #
# Homework number 3                                                                                                    #
# OOP python                                                                                                           #
# Problem 11                                                                                                           #
#                                                                                                                      #
# The code does the following:                                                                                         #
# - it has a player as a dot                                                                                           #
# - it has another dot which is the enemy/computer which follows the player                                            #
# - it has treasures, but not friends                                                                                  #
# - it has and end point                                                                                               #
#                                                                                                                      #
# The code lacks the following:                                                                                        #
# - uppon pressing "q" the game does not stop, but it does stop when pressing "Esc"                                    #
# - does not have friends                                                                                              #
# - does not have show_location function                                                                               #
# - does not have fight mechanic                                                                                       #
# - does not have health bar                                                                                           #
# - does not have doors                                                                                                #
# - does not have another map which can be accesed by entering a door or a point                                       #
# - does not have help button                                                                                          #
# - does not have save/load buttons                                                                                    #
# - does not have drop treasure                                                                                        #
# - does not have different types of rooms, as well as not having a class Room                                         #
#                                                                                                                      #
# Basically it is a simple maze game simulating a escape mode                                                          #
# With points needed to be gathered in order to finish the maze, while stepping into the end point                     #
# It uses OOP, not everything related to OOP                                                                           #
#                                                                                                                      #
########################################################################################################################

#this function puts the window of the game in a certain position on the screen
def set_window_position(x, y):

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

#this function creates the map
def create_grid(size):

    grid = Graph() #an object grid of type Graph initialized by the default constructor of class Graph
    #creates a graph for the grid/map

    #loop to add vertices to the grid/map
    for i in range(size):
        for j in range(size):
            grid.add_vertex((i, j))

    #returns the grid/map
    return grid

#this function creates the walls and the path from start to finish, basically the maze itself
def create_maze(grid, vertex, completed=None, vertices=None):

    if vertices is None:
        vertices = grid.get_vertices()
    if completed is None:
        completed = [vertex]

    #the following two lines are making a random path each iteration/each time the game starts
    paths = list(int(i) for i in range(4))
    random.shuffle(paths)

    #the direction of vertex after vertex
    up = (vertex[0], vertex[1] - 1)
    down = (vertex[0], vertex[1] + 1)
    left = (vertex[0] - 1, vertex[1])
    right = (vertex[0] + 1, vertex[1])

    #adding edges
    for direction in paths:
        if direction == 0:
            if up in vertices and up not in completed:
                grid.add_edge((vertex, up))
                grid.add_edge((up, vertex))
                completed.append(up)
                create_maze(grid, up, completed, vertices)
        elif direction == 1:
            if down in vertices and down not in completed:
                grid.add_edge((vertex, down))
                grid.add_edge((down, vertex))
                completed.append(down)
                create_maze(grid, down, completed, vertices)
        elif direction == 2:
            if left in vertices and left not in completed:
                grid.add_edge((vertex, left))
                grid.add_edge((left, vertex))
                completed.append(left)
                create_maze(grid, left, completed, vertices)
        elif direction == 3:
            if right in vertices and right not in completed:
                grid.add_edge((vertex, right))
                grid.add_edge((right, vertex))
                completed.append(right)
                create_maze(grid, right, completed, vertices)

    return grid

#this functions takes the stored information by the above functions
#and then "draws" the maze on the map of length x width size using a predefined colour (black)
def draw_maze(screen, maze, size, colour, side_length, border_width):

    #for each vertex in the maze
    for i in range(size):
        for j in range(size):
            if (i != 0):
                #if the vertex is not at the left-most side of the map
                if maze.is_edge(((i, j), (i - 1, j))):
                    #check if the grid unit to the current unit's left is connected by an edge
                    #if connected, draw the grid unit without the left wall
                    pygame.draw.rect(screen, colour,[(side_length + border_width) * i, border_width + (side_length + border_width) * j, side_length + border_width, side_length])
            if (i != size - 1):#right-most side of the map
                if maze.is_edge(((i, j), (i + 1, j))):#check
                    #draw
                    pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, border_width + (side_length + border_width) * j,side_length + border_width, side_length])
            if (j != 0):#top-most side of the map
                if maze.is_edge(((i, j), (i, j - 1))):#check
                    #draw
                    pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, (side_length + border_width) * j, side_length,side_length + border_width])
            if (j != size - 1):#bottom-most side of the map
                if maze.is_edge(((i, j), (i, j + 1))):#check
                    #draw
                    pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * i, border_width + (side_length + border_width) * j, side_length,side_length + border_width])

#draw position of grid unit
def draw_position(screen, side_length, border_width, current_point, colour):

    pygame.draw.rect(screen, colour, [border_width + (side_length + border_width) * current_point[0], border_width + (side_length + border_width) * current_point[1], side_length,side_length])

#this function updates the path of the a said point
def update_path(next_point, deque):

    if len(deque) >= 2:
        first_pop = deque.pop()#current point before moving
        second_pop = deque.pop()#previous point
        if second_pop == next_point:
            #only append the previous point
            deque.append(second_pop)
        else:
            #add all the points including the next one
            deque.append(second_pop)
            deque.append(first_pop)
            deque.append(next_point)
        return deque
    else:
        #if there is just the initial point
        deque.append(next_point)
        return deque

#this uses the above function, but this time it updates the enemy chasing you
def update_path_map_points(start_point, end_point, maze, deque):

    closest_path = map_points.map_points(start_point, end_point, maze)

    closest_path.remove(start_point)
    if len(deque) + 1 > len(closest_path):
        deque.clear()
        for edge in closest_path:
            deque.append(edge)
        return deque
    else:
        return update_path(end_point, deque)

#this functions breaks a wall, the wall breaks by holding spacebar and the arrow which shows the direction
def break_wall(maze, current_point, next_point):

    if not maze.is_edge((current_point, next_point)):
        maze.add_edge((current_point, next_point))
        maze.add_edge((next_point, current_point))

    return maze

#updates the console
def update_console(screen, screen_size, side_length, text_size, a_colour, na_colour, keys_left, wallBreaks):

    if keys_left == 0:
        text = "This is the way: " + " WB: " + str(wallBreaks)
    else:
        text = "Treasures left: " + str(keys_left) + " WB: " + str(wallBreaks)

    console_rect = (0, screen_size[1] - side_length * 3, screen_size[0], side_length * 3)
    pygame.draw.rect(screen, na_colour, console_rect)

    displayText = pygame.font.SysFont("ubuntu", text_size)
    textSurface = displayText.render(text, True, a_colour)
    textRect = textSurface.get_rect()
    textRect.center = (screen_size[0] / 2, screen_size[1] - text_size * 2)

    screen.blit(textSurface, textRect)
    pygame.display.update(console_rect)

#the core function which basically runs the game
def runGame(grid_size, side_length, mode):

    #initialize the game
    pygame.init()

    #colours for different buttons etc.
    BLACK = (0, 0, 0)
    LIGHTRED = (255, 100, 100)
    WHITE = (255, 255, 255)
    LIGHTGREEN = (0, 255, 0)
    GREEN = (0, 200, 0)
    RED = (205, 0, 0)


    border_width = side_length // 5 #scales the width according to the length
    grid = create_grid(grid_size) #initialize the map
    maze = create_maze(grid, (grid_size // 2, grid_size // 2))#initialize the walls
    #setting the size of the screen to match the map
    size = (grid_size * (side_length + border_width) + border_width, grid_size * (side_length + border_width) + border_width)

    #if mode == 4: # there is only one mode
       #size = (size[0], size[1] + side_length * 3)

    screen = pygame.display.set_mode(size)#initialize the screen
    pygame.display.set_caption("\"Esc\" to exit")#title of the app when in-game

    carryOn = True #condition for loop
    clock = pygame.time.Clock()#screen update
    screen.fill(BLACK)#black background

    vertices = maze.get_vertices()#initalize the vertices
    draw_maze(screen, maze, grid_size, WHITE, side_length, border_width)#draws the walls

    start_point = (0, 0)#start point of the player
    end_point = (grid_size - 1, grid_size - 1)#end point

    choice = random.randrange(4)#random end point and start point

    if choice == 0:
        start_point = (grid_size - 1, grid_size - 1)
        end_point = (0, 0)
    elif choice == 1:
        start_point = (0, grid_size - 1)
        end_point = (grid_size - 1, 0)
    elif choice == 2:
        start_point = (grid_size - 1, 0)
        end_point = (0, grid_size - 1)

    winner = 0 # winner variable, decides the outcome of the game
    #an object called player1 of class Character initialized by default constructor which defines the player itself
    player1 = Character(screen, side_length, border_width, vertices, start_point, end_point, start_point, GREEN, WHITE)


    if mode == 4:

        x_coords = random.sample(range(1, grid_size - 1), 3)#number of treasures in order to be able
        y_coords = random.sample(range(1, grid_size - 1), 3)#to enter the end point, to win the game

        unlock_keys = []

        for i in range(3):#adds the treasures
            unlock_keys.append((x_coords[i], y_coords[i]))

        #re-initialize character and enemy
        player1 = Character(screen, side_length, border_width, vertices, start_point, end_point, start_point, GREEN, WHITE, True, unlock_keys, LIGHTGREEN)
        computer_character = Character(screen, side_length, border_width, vertices, start_point, end_point, start_point, LIGHTRED, WHITE)

        dq = deque()
        dq.append(start_point)

        computer_cooldown = grid_size * 100
        if computer_cooldown > 3000: # how much time the enemy waits before following you
            computer_cooldown = 3000

        initial_wait = 3000
        computer_timer = pygame.time.get_ticks()
        initial_wait_timer = pygame.time.get_ticks()

    draw_position(screen, side_length, border_width, end_point, RED)#end point

    if mode == 4:#updates the map, draws treasures
        player1.draw_keys()
        update_console(screen, size, side_length, size[0] // grid_size, WHITE, BLACK, player1.get_keys_left(),player1.get_wallBreaks())

    pygame.display.flip()#screen update
    cooldown = 100 #timer for pressing arrows
    start_timer = pygame.time.get_ticks() #initalize cooldown timer

    while carryOn: #core loop

        for event in pygame.event.get():#if player does something
            if event.type == pygame.QUIT:
                carryOn = False
                mode = -1 #exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carryOn = False
                    mode = -1

        #stores the arrows pressed
        keys = pygame.key.get_pressed()

        if (pygame.time.get_ticks() - start_timer > cooldown):#moves the player in the chosen direction
            current_point = player1.get_current_position()#get the current location
            if keys[pygame.K_RIGHT]:#moves the character right
                if (current_point[0] + 1, current_point[1]) in vertices:#checks if the next point is in the maze
                    next_point = (current_point[0] + 1, current_point[1])
                    if (maze.is_edge((current_point, next_point))):#check if next point is connected by an edge
                        player1.move_character_smooth(next_point, 5)
                        if mode == 4:#updates enemy path
                            dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                    else:
                        if mode == 4:#breaks wall
                            if keys[pygame.K_SPACE] and player1.get_wallBreaks() > 0:
                                maze = break_wall(maze, current_point, next_point)
                                player1.move_character_smooth(next_point, 5)
                                player1.use_wallBreak()
                                #updates path of enemy after the wall breaks
                                dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                start_timer = pygame.time.get_ticks()#restarts cooldown timer
                #next lines do the same thing but for left, up and down direction
            elif keys[pygame.K_LEFT]:
                if (current_point[0] - 1, current_point[1]) in vertices:
                    next_point = (current_point[0] - 1, current_point[1])
                    if (maze.is_edge((current_point, next_point))):
                        player1.move_character_smooth(next_point, 5)
                        if mode == 4:
                            dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                    else:
                        if mode == 4:
                            if keys[pygame.K_SPACE] and player1.get_wallBreaks() > 0:
                                maze = break_wall(maze, current_point, next_point)
                                player1.move_character_smooth(next_point, 5)
                                player1.use_wallBreak()
                                dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                start_timer = pygame.time.get_ticks()
            elif keys[pygame.K_UP]:
                if (current_point[0], current_point[1] - 1) in vertices:
                    next_point = (current_point[0], current_point[1] - 1)
                    if (maze.is_edge((current_point, next_point))):
                        player1.move_character_smooth(next_point, 5)
                        if mode == 4:
                            dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                    else:
                        if mode == 4:
                            if keys[pygame.K_SPACE] and player1.get_wallBreaks() > 0:
                                maze = break_wall(maze, current_point, next_point)
                                player1.move_character_smooth(next_point, 5)
                                player1.use_wallBreak()
                                dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                start_timer = pygame.time.get_ticks()
            elif keys[pygame.K_DOWN]:
                if (current_point[0], current_point[1] + 1) in vertices:
                    next_point = (current_point[0], current_point[1] + 1)
                    if (maze.is_edge((current_point, next_point))):
                        player1.move_character_smooth(next_point, 5)
                        if mode == 4:
                            dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                    else:
                        if mode == 4:
                            if keys[pygame.K_SPACE] and player1.get_wallBreaks() > 0:
                                maze = break_wall(maze, current_point, next_point)
                                player1.move_character_smooth(next_point, 5)
                                player1.use_wallBreak()
                                dq = update_path_map_points(computer_character.get_current_position(), next_point, maze, dq)
                start_timer = pygame.time.get_ticks()

        if mode == 4:#enemy movement
            player1.draw_keys()
            if player1.collected_all():#if the player colected all the treasure the end point will change colour
                draw_position(screen, side_length, border_width, end_point, GREEN)#telling the player
                #that it is time to go through the end point to win the game
            else:
                draw_position(screen, side_length, border_width, end_point, RED)
            update_console(screen, size, side_length, size[0] // grid_size, WHITE, BLACK, player1.get_keys_left(),player1.get_wallBreaks())

        waitCondition = pygame.time.get_ticks() - initial_wait_timer > initial_wait
        if (waitCondition):
            if (pygame.time.get_ticks() - computer_timer > computer_cooldown):
                if dq:
                    computer_character.move_character_smooth(dq.popleft(), 5)
                computer_timer = pygame.time.get_ticks()

        computer_character.draw_position()
        player1.draw_position()
        pygame.display.update()

        if mode == 4:#win condition using the winner variable which decides the outcome
            if player1.escaped():
                winner = 1
                carryOn = False
            elif computer_character.get_current_position() == player1.get_current_position() and waitCondition:
                winner = 2
                carryOn = False

        clock.tick(60)#60 fps

    pygame.quit()#quit
    return mode, winner

if __name__ == "__main__":

    #puts the window of the game in the desired position
    set_window_position(100, 150)

    #initializes the application
    states = {0: "Main Menu", 1: "Gameplay"}
    current_state = states[0]

    grid_size = 0
    side_length = 0
    mode = 0

    Run = True #main loop condition
    #main loop
    while Run:#initalizes loop
        if current_state == states[0]:
            Run, grid_size, side_length, mode = user_interface.startScreen()
            current_state = states[1]
        elif current_state == states[1]:
            mode, value = runGame(grid_size, side_length, mode)
            if mode != -1:
                user_interface.endGame(mode, value)

            current_state = states[0]

    quit()