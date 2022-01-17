import pygame
import time

#user interface file
#used to define everything that belongs to the interface of the application

#this functions is used to display text on screen
def displayMessage(text, colour, screen, size, screen_size, y_pos, screen_update=None):

    displayText = pygame.font.SysFont("ubuntu", size)
    textSurface = displayText.render(text, True, colour)
    textRect = textSurface.get_rect()
    textRect.center = ((screen_size[0]/2), y_pos)

    screen.blit(textSurface,textRect)

    if screen_update is None:
        screen_update = textRect
    pygame.display.update(screen_update)

#this aplication displays the main menu, the settings menu, with three buttons: start, settings, exit
def displayMenuSelection(screen, screen_size, choice, bg_colour, a_colour, na_colour):

    screen.fill(bg_colour)

    if choice == 0:
        displayMessage("The Maze Game", na_colour, screen, 60, screen_size, screen_size[1]//5)
        displayMessage("Start", a_colour, screen, 50, screen_size, screen_size[1]*2//5)
        displayMessage("Settings", na_colour, screen, 50, screen_size, screen_size[1]*3//5)
        displayMessage("Quit", na_colour, screen, 50, screen_size, screen_size[1]*4//5)
    elif choice == 1:
        displayMessage("The Maze Game", na_colour, screen, 60, screen_size, screen_size[1]//5)
        displayMessage("Start", na_colour, screen, 50, screen_size, screen_size[1]*2//5)
        displayMessage("Settings", a_colour, screen, 50, screen_size, screen_size[1]*3//5)
        displayMessage("Quit", na_colour, screen, 50, screen_size, screen_size[1]*4//5)
    elif choice == 2:
        displayMessage("The Maze Game", na_colour, screen, 60, screen_size, screen_size[1]//5)
        displayMessage("Start", na_colour, screen, 50, screen_size, screen_size[1]*2//5)
        displayMessage("Settings", na_colour, screen, 50, screen_size, screen_size[1]*3//5)
        displayMessage("Quit", a_colour, screen, 50, screen_size, screen_size[1]*4//5)

#this functions displays the settings available and a return button on screen
def displaySettingsSelection(screen, screen_size, choice, bg_colour, a_colour, na_colour, grid_size, side_length, mode):

    screen.fill(bg_colour)
    grid_text = "Grid size: " + str(grid_size)
    side_text = "Side length: " + str(side_length)

    if choice == 0:
        displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
        displayMessage(grid_text, a_colour, screen, 30, screen_size, screen_size[1]*2//6)
        displayMessage(side_text, na_colour, screen, 30, screen_size, screen_size[1]*3//6)
        displayMessage("Return", na_colour, screen, 30, screen_size, screen_size[1]*5//6)
    elif choice == 1:
        displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
        displayMessage(grid_text, na_colour, screen, 30, screen_size, screen_size[1]*2//6)
        displayMessage(side_text, a_colour, screen, 30, screen_size, screen_size[1]*3//6)
        displayMessage("Return", na_colour, screen, 30, screen_size, screen_size[1]*5//6)
    elif choice == 2:
        displayMessage("Settings", na_colour, screen, 60, screen_size, screen_size[1]//6)
        displayMessage(grid_text, na_colour, screen, 30, screen_size, screen_size[1]*2//6)
        displayMessage(side_text, na_colour, screen, 30, screen_size, screen_size[1]*3//6)
        displayMessage("Return", a_colour, screen, 30, screen_size, screen_size[1]*5//6)

#this initializes the menu and all the available buttons
def settingsMenu(screen, screen_size, bg_colour, a_colour, na_colour, cooldown, start_timer, g_size, s_length):

    options = {0:"Grid Size", 1:"Side Length", 2:"Return", 3:"Mode"} #buttons
    modes = {4:"Escape"} #there is only one mode

    current_mode = 4 #mode variable
    current_selection = options[0]
    grid_size = g_size
    side_length = s_length

    pygame.display.set_caption("Settings")
    screen.fill(bg_colour)
    pygame.display.flip()
    displaySettingsSelection(screen, screen_size, 0, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])

    carryOn = True

    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
                Run = False

        keys = pygame.key.get_pressed()

        if (pygame.time.get_ticks() - start_timer > cooldown):
            if current_selection == options[0]:
                if keys[pygame.K_DOWN]:
                    displaySettingsSelection(screen, screen_size, 1, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[1]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_LEFT]:
                    grid_size -= 1
                    if grid_size < 10:
                        grid_size = 10
                    displaySettingsSelection(screen, screen_size, 0, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RIGHT]:
                    grid_size += 1
                    if grid_size > 35:
                        grid_size = 35
                    displaySettingsSelection(screen, screen_size, 0, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
            elif current_selection == options[1]:
                if keys[pygame.K_DOWN]:
                    displaySettingsSelection(screen, screen_size, 2, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[2]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_UP]:
                    displaySettingsSelection(screen, screen_size, 0, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[0]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_LEFT]:
                    side_length -= 1
                    if side_length < 10:
                        side_length = 10
                    displaySettingsSelection(screen, screen_size, 1, bg_colour, a_colour, na_colour,grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RIGHT]:
                    side_length += 1
                if side_length > 15:
                    side_length = 15
                    displaySettingsSelection(screen, screen_size, 1, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
            elif current_selection == options[2]:
                if keys[pygame.K_DOWN]:
                    displaySettingsSelection(screen, screen_size, 3, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[3]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_UP]:
                    displaySettingsSelection(screen, screen_size, 1, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[1]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_LEFT]:
                    current_mode -= 1
                    if current_mode < 0:
                        current_mode = 0
                    displaySettingsSelection(screen, screen_size, 2, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RIGHT]:
                    current_mode += 1
                    if current_mode > 4:
                        current_mode = 4
                    displaySettingsSelection(screen, screen_size, 2, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    start_timer = pygame.time.get_ticks()
            elif current_selection == options[3]:
                if keys[pygame.K_UP]:
                    displaySettingsSelection(screen, screen_size, 2, bg_colour, a_colour, na_colour, grid_size, side_length, modes[current_mode])
                    current_selection = options[2]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RETURN]:
                    carryOn = False

    pygame.display.set_caption("Main Menu")
    return grid_size, side_length, current_mode

#this functions designs the main menu
def startScreen():

    pygame.init()

    grid_size = 20
    side_length = 10

    BLACK = (255,255,255)
    WHITE = (0, 0, 0)
    PURPLE = (102, 0, 103)

    screen_size = (1080,720)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Main Menu")
    screen.fill(WHITE)

    pygame.display.flip()
    displayMenuSelection(screen, screen_size, 0, WHITE, PURPLE, BLACK)

    options = {0:"Start Game", 1:"Settings", 2:"Exit"}
    current_selection = options[0]
    clock = pygame.time.Clock()
    mode = 0
    Run = True
    carryOn = True
    Settings = False
    cooldown = 150

    start_timer = pygame.time.get_ticks()

    while carryOn:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                carryOn = False
                Run = False

        keys = pygame.key.get_pressed()

        if (pygame.time.get_ticks() - start_timer > cooldown):
            if current_selection == options[0]:
                if keys[pygame.K_DOWN]:
                    displayMenuSelection(screen, screen_size, 1, WHITE, PURPLE, BLACK)
                    current_selection = options[1]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RETURN]:
                    carryOn = False
            elif current_selection == options[1]:
                if keys[pygame.K_UP]:
                    displayMenuSelection(screen, screen_size, 0, WHITE, PURPLE, BLACK)
                    current_selection = options[0]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_DOWN]:
                    displayMenuSelection(screen, screen_size, 2, WHITE, PURPLE, BLACK)
                    current_selection = options[2]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RETURN]:
                    Settings = True
            elif current_selection == options[2]:
                if keys[pygame.K_UP]:
                    displayMenuSelection(screen, screen_size, 1, WHITE, PURPLE, BLACK)
                    current_selection = options[1]
                    start_timer = pygame.time.get_ticks()
                if keys[pygame.K_RETURN]:
                    carryOn = False
                    Run = False

        if Settings:
            grid_size, side_length, mode = settingsMenu(screen, screen_size, WHITE, PURPLE, BLACK, cooldown, start_timer, grid_size, side_length)
            current_selection = options[0]
            displayMenuSelection(screen, screen_size, 0, WHITE, PURPLE, BLACK)
            pygame.display.flip()
            time.sleep(0.25)
            start_timer = pygame.time.get_ticks()
            Settings = False

        clock.tick(60)

    pygame.quit()
    return Run, grid_size, side_length, mode

#this functions designs the way the end of the game screen looks
def endGame(mode, value):

    pygame.init()

    BLACK = (255,255,255)
    WHITE = (0, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 127)

    screen_size = (1080,720)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption("Game Over")
    screen.fill(WHITE)
    pygame.display.flip()


    if mode == 4:
        displayMessage("Game Over", BLACK, screen, 60, screen_size, screen_size[1]//4)
        if value == 1:
            text = "You win"
            displayMessage(text, BLUE, screen, 50, screen_size, screen_size[1]*2//4)
        else:
            text = "You lost!"
            displayMessage(text, GREEN, screen, 50, screen_size, screen_size[1]*2//4)
        displayMessage("Press enter to exit to menu.", BLACK, screen, 20, screen_size,screen_size[1]*3//4)

    carryOn = True
    clock = pygame.time.Clock()

    while carryOn:
        for event in pygame.event.get():# user did something
            if event.type == pygame.QUIT:
                carryOn = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            carryOn = False

        clock.tick(60)
    pygame.quit()
