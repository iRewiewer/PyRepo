import pygame
from pygame.locals import *
from pygame.font import *

def highscores(screen, window_size, background_color, colors, fonts):
    # Set text colors
    text_color = colors["white"] # Color of all text
    text_bg = colors["black"] # The background of each label
    
    # Set fonts used
    title_font = Font(fonts["Scream"], 62) # Title text font
    score_font = Font(fonts["LCD"], 42) # Every scores's font

    # Constants that determine the menu buttons' positions (y axis)
    base_pos = 120
    const = 60 # The constant distance between each button

    screen.fill(background_color)
    
    # Title Label
    title = title_font.render("Highscores", True, text_color, text_bg)
    title_object = title.get_rect()
    title_object.center = (window_size[0] // 2, 75)  # Set the title label position in the top middle of the window
    screen.blit(title, title_object)

    # Read all the highscores from the respective file
    try:
        file = open("highscores.yml", "r")
        
        highscores_list = file.read()
        highscores_list = highscores_list.split("\n")

        for i in range (0, len(highscores_list)):
            highscores_list[i] = highscores_list[i].split(":")

    except:
        raise("Error: Line 30, highscores.py, Error reading highschores from file.")

    finally:
        file.close()

    # Draw each one of the highscores
    try:
        for i in range (0, 12):
            # Initialize score object
            score = score_font.render(str(highscores_list[i][0]) + " " + str(highscores_list[i][1]), True, text_color, text_bg)
            score_object = score.get_rect()
            
            # Draw it into respective column
            if i < 6: score_object = score_object.move(165, base_pos + (i + 1) * const) # Column 1
            else: score_object = score_object.move(645, base_pos + (i - 5) * const) # Column 2

            screen.blit(score, score_object)  
    except:
        raise("Error: Line 55, highscores.py, Error drawing highscores")
    
    # Updates entire screen
    pygame.display.flip()

    # Return to main menu upon pressing a key
    quit = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                quit = True

        if quit == True: break