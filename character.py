import pygame
from time import sleep

#character class

class Character:

    def __init__(self, screen, side_length, border_width, valid_points, start_point, end_point, current_position, a_colour, na_colour, escape=False, keys=None, k_colour=None):

        #default constructor
        self.screen = screen
        self.side_length = side_length
        self.border_width = border_width
        self.start_point = start_point
        self.end_point = end_point
        self.current_position = current_position
        self.a_colour = a_colour
        self.na_colour = na_colour
        self.escape = escape
        self.keys = keys
        self.k_colour = k_colour
        self.unlocked = False
        self.wallBreaks = 1
        self.increaseCompSpeed = False
        self.draw_position()

    def draw_position(self):#draws position of player

        pygame.draw.rect(self.screen, self.a_colour,[self.border_width + (self.side_length + self.border_width) * self.current_position[0],self.border_width + (self.side_length + self.border_width) * self.current_position[1],self.side_length, self.side_length])

    def move_character(self, next_position):#moves the character

        current_rect = [self.border_width + (self.side_length + self.border_width) * self.current_position[0], self.border_width + (self.side_length + self.border_width) * self.current_position[1], self.side_length, self.side_length]
        next_rect = [self.border_width + (self.side_length + self.border_width) * next_position[0],self.border_width + (self.side_length + self.border_width) * next_position[1],self.side_length, self.side_length]

        pygame.draw.rect(self.screen, self.na_colour, current_rect)
        pygame.display.update(current_rect)
        pygame.draw.rect(self.screen, self.a_colour, next_rect)
        pygame.display.update(next_rect)

        self.current_position = next_position
        if self.escape is True:
            if self.current_position in self.keys:
                self.keys.remove(self.current_position)
                if len(self.keys) % 2 == 0:
                    self.wallBreaks += 1
                    self.increaseCompSpeed = True

    def move_character_smooth(self, next_position, steps):

        if next_position[0] != self.current_position[0]:
            for i in range(1, steps + 1):
                sleep(0.005)
                difference = (next_position[0] - self.current_position[0]) * i / steps
                next_pos = (self.current_position[0] + difference, self.current_position[1])
                self.move_character(next_pos)
        else:
            for i in range(1, steps + 1):
                sleep(0.005)
                difference = (next_position[1] - self.current_position[1]) * i / steps
                next_pos = (self.current_position[0], self.current_position[1] + difference)
                self.move_character(next_pos)

    def get_current_position(self):

        return self.current_position

    def reached_goal(self):

        if self.current_position == self.end_point:
            return True
        else:
            return False

    def get_wallBreaks(self):

        return self.wallBreaks

    def use_wallBreak(self):

        self.wallBreaks -= 1

    def get_keys_left(self):

        if self.keys:
            return len(self.keys)
        else:
            return 0

    def draw_keys(self):

        for key in self.keys:

            pygame.draw.rect(self.screen, self.k_colour,[self.border_width + (self.side_length + self.border_width) * key[0], self.border_width + (self.side_length + self.border_width) * key[1], self.side_length,self.side_length])

    def increase_computer_speed(self):

        if self.increaseCompSpeed:
            self.increaseCompSpeed = False
            return True
        else:
            return False

    def collected_all(self):#if collects every treasure

        if not self.keys:
            self.unlocked = True
            return True
        else:
            return False

    def escaped(self):#if win

        if self.unlocked is True and self.reached_goal():
            return True
        else:
            return False