### Libraries ###
import sys, pygame
from pygame.locals import *
from pygame.font import *
from random import random as rng

from game import game_setup
from highscores import highscores
from entities import Game

#### This file represents the menu before starting the game ####

### Window Settings ###
pygame.init()
pygame.display.set_caption('Pong')
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

# Setting screen_object size (window_size) to 1000x600
try:
    window_size = 1000, 600
    screen_object = pygame.display.set_mode(window_size)
except:
    raise("Error: Line 21, pong.py, screen_object Size Setting Error")
    
# Color pallete declaration which will be used throughout the program
colors = {
            "black":(0, 0, 0),
            "white":(255,255,255),
            "random":(int(rng() * 1000 % 256), int(rng() * 1000 % 256), int(rng() * 1000 % 256) )
         }

fonts = {
            "Scream":'assets/fonts/Scream.ttf',
            "LCD":'assets/fonts/LCD.ttf',
         }

menu = Game(screen_object, window_size, colors, fonts, 60, 1)

# Clock is used to set the application's framerate
clock = pygame.time.Clock()

# Set fonts used
title_font = Font(fonts["Scream"], 72) # Title text font
button_font = Font(fonts["LCD"], 32) # Every button's font
credits_font = Font(fonts["LCD"], 14) # Credits font

# The menu opens with the first button being selected
button = 0

# Constants that determine the menu buttons' positions (y axis)
base_pos = 230
const = 70 # The constant distance between each button

# Title Label
title = title_font.render("PONG", True, menu.text_color, menu.text_background_color)
title_object = title.get_rect()
title_object.center = (window_size[0] // 2, 100) # Set the title label position in the top middle of the window

# Credits Label
credits = credits_font.render("Made by iRewiewer", True, menu.text_color, menu.text_background_color)
credits_object = credits.get_rect()
credits_object.center = (80, window_size[1] - 10) # Set the credits label position in the bottom right corner of the window 

while True:
    # Set the FPS at which the menu runs - 30 seems to be enough to not feel laggy
    clock.tick(30)

    # Get an array of all keys pressed
    keys_pressed = pygame.key.get_pressed()
    
    # Loop through all events and look for key events
    for event in pygame.event.get():
    
        # If an exit event has been triggered, close the application
        if ((keys_pressed[pygame.K_RALT] or keys_pressed[pygame.K_LALT]) and keys_pressed[pygame.K_F4]) or keys_pressed[pygame.K_ESCAPE]: sys.exit()         
        if event.type == pygame.QUIT: sys.exit()
        
        ## The default button state is 0 - being the singleplayer button
        # button state 1 is multiplayer (local coop)
        # button state 2 is endless mode
        # button state 3 is highscores 
        # button state 4 is exit

        # Previous button
        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            if button != 0: button -= 1
            else: button = 4
        
        # Next button
        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            if button != 4: button += 1
            else: button = 0

    # Singleplayer button on/off state
    if button == 0:
        button0 = button_font.render(">> 1 Player <<", True, menu.text_color, menu.text_background_color)
        if keys_pressed[pygame.K_RETURN]:
            game_setup(screen_object, window_size, colors, fonts, "singleplayer")
    else:
        button0 = button_font.render("1 Player", True, menu.text_color, menu.text_background_color)
    
    # Multiplayer button on/off state
    if button == 1:
        button1 = button_font.render(">> 2 Players <<", True, menu.text_color, menu.text_background_color)
        if keys_pressed[pygame.K_RETURN]:
            game_setup(screen_object, window_size, colors, fonts, "multiplayer")
    else:
        button1 = button_font.render("2 Players", True,  menu.text_color, menu.text_background_color)
    
    # Endless button on/off state
    if button == 2:
        button2 = button_font.render(">> Endless <<", True, menu.text_color, menu.text_background_color)
        if keys_pressed[pygame.K_RETURN]:
            game_setup(screen_object, window_size, colors, fonts, "endless")
    else:
        button2 = button_font.render("Endless", True, menu.text_color, menu.text_background_color)
    
    # Highscores button on/off state
    if button == 3:
        button3 = button_font.render(">> Highscores <<", True, menu.text_color, menu.text_background_color)
        if keys_pressed[pygame.K_RETURN]:
            highscores(screen_object, window_size, menu.text_background_color, colors, fonts)
    else:
        button3 = button_font.render("Highscores", True, menu.text_color, menu.text_background_color)
    
    # Exit button on/off state
    if button == 4:
        button4 = button_font.render(">> Exit <<", True, menu.text_color, menu.text_background_color)
        if keys_pressed[pygame.K_RETURN]:
            # Exit the application
            sys.exit()
    else:
        button4 = button_font.render("Exit", True, menu.text_color, menu.text_background_color)

    # Set menu buttons's positions
    button0_object = button0.get_rect()
    button0_object.center = (window_size[0] // 2, base_pos + const * 0)
    button1_object = button1.get_rect()
    button1_object.center = (window_size[0] // 2, base_pos + const * 1)
    button2_object = button2.get_rect()
    button2_object.center = (window_size[0] // 2, base_pos + const * 2)
    button3_object = button3.get_rect()
    button3_object.center = (window_size[0] // 2, base_pos + const * 3)    
    button4_object = button4.get_rect()
    button4_object.center = (window_size[0] // 2, base_pos + const * 4)
    
    # Display the elements on the screen
    screen_object.fill(menu.text_background_color)
    screen_object.blit(title, title_object)
    screen_object.blit(credits, credits_object)
    screen_object.blit(button0, button0_object)
    screen_object.blit(button1, button1_object)
    screen_object.blit(button2, button2_object)
    screen_object.blit(button3, button3_object)
    screen_object.blit(button4, button4_object)

    # Updates entire screen_object
    pygame.display.flip()