import pygame, sys, os
from datetime import datetime as dtime

# Define app options
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([370,480])
pygame.display.set_caption('ChstAutoDB')
pygame.display.set_icon(pygame.image.load('car.png'))

# Define file creating function
def create_files():
    # Read config.yml
    # Create it if it doesnt exist
    try:
        file = open("config.yml", "r")
    except FileNotFoundError as e:
        print("Error: " + str(e))
        print("Creating config.yml ...")
        os.system("echo 1 > config.yml")

    # Try reading the scores database
    # and creates a null one if it doesn't exist already
    try:
        file = open("scores.db", "r")
    except FileNotFoundError as e:
        print("Error: " + str(e))
        print("Creating scores.db ...")
        os.system("type nul > scores.db")

# Initial Run
create_files()

# Define app assets

# Read the index in the config file
file = open("config.yml", "r")
in_file = list(file.read())
index = int(in_file[0])
file.close()

# Font
base_font = pygame.font.Font('LCD.ttf', 32)
credits_font = pygame.font.Font('LCD.ttf', 14)

# Text fields
label_title = 'ChstAutoDB'
label_credits = 'by iRewiewer'
label_score = 'S'
label_reset = 'R'
label_points = 'Points:'
label_pass = 'Pass?'
label_datetime = 'Timestamp:'
submit_button = 'Submit'
user_points = '       '
label_version = 'v1.0'

# Sprites
check_sprite = pygame.image.load('check.png')
cross_sprite = pygame.image.load('cross.png')

# Rectangles
title_rect = pygame.Rect(90,20,200,50)
credits_rect = pygame.Rect(235,55,20,20)
score_rect = pygame.Rect(5,5,32,37)
reset_rect = pygame.Rect(332,5,32,37)
label_points_rect = pygame.Rect(10,100,200,50)
user_points_rect = pygame.Rect(160,90,200,50)
label_pass_rect = pygame.Rect(10,170,200,50)
check_sprite_rect = check_sprite.get_rect()
check_sprite_rect = check_sprite_rect.move(130,150)
cross_sprite_rect = cross_sprite.get_rect()
cross_sprite_rect = cross_sprite_rect.move(130,150)
label_datetime_rect = pygame.Rect(10,240,200,50)
user_date_rect = pygame.Rect(10,300,200,50)
user_time_rect = pygame.Rect(10,350,200,50)
submit_button_rect = pygame.Rect(80,400,200,50)
label_version_rect = pygame.Rect(330,465,50,50)

# Colors
color_active = pygame.Color('firebrick3')
color_passive = pygame.Color('gray15')
user_points_color = color_passive
submit_button_color = color_passive
score_button_color = color_passive
reset_button_color = color_passive

# Field press checker
user_points_border = False
submit_button_border = False
score_border = False
reset_border = False

# First digit >2 flagger
too_big_points = False

# Timer for border color change
submit_button_press_timer = 0
score_button_press_timer = 0
reset_button_press_timer = 0
points = 0

# Used for testing if the first digit is bigger
# than 2 and if the user is typing digits at all
big_digits = [pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
all_digits = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

while True:
    # Real time update to date & time
    user_date = dtime.now().strftime('%a, %d %b %Y')
    user_time = dtime.now().strftime('%H:%M:%S')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clicked on points user input box - change border color
            if user_points_rect.collidepoint(event.pos):
                user_points_border = True
            else:
                user_points_border = False
            
            # Clicked on the 'Submit' button - add to scores database
            if submit_button_rect.collidepoint(event.pos):
                submit_button_border = True
                
                # Append to the database file
                file = open("scores.db", "a")
                
                if len(user_points) > 7:
                    if int(points) >= 22: verdict = "Pass"
                    else: verdict = "Fail"

                    file.write("Quiz No. " + str(index) + " - " + str(points) + " points - " + verdict + " - " + user_time + " " + user_date + "\n")
                    
                    index += 1
                    
                    # Write back the increased index
                    file = open("config.yml", "w")
                    file.write(str(index))
                    file.close()

                
                # Reset the points variable and the user_points field text
                points = 0
                user_points = '       '
                too_big_points = False
                
                submit_button_press_timer = 0
            else:
                submit_button_border = False
            
            # Clicked on the 'S' button - show scores database
            if score_rect.collidepoint(event.pos):

                os.system("notepad scores.db")

                score_border = True
                score_button_press_timer = 0
            else:
                score_border = False
                
            # Clicked on the 'R' button - reset the config and scores files
            if reset_rect.collidepoint(event.pos):
                
                index = 1
                
                os.system("del config.yml")
                os.system("del scores.db")
                
                create_files()
                
                reset_border = True
                reset_button_press_timer = 0
            else:
                reset_border = False
                
        # once a key is pressed
        if event.type == pygame.KEYDOWN:
            # if user text box is active
            if user_points_border == True:
                # if the user wants to delete a character
                if event.key == pygame.K_BACKSPACE and len(user_points) >= 8:
                    # if its the first character
                    if len(user_points) == 8:
                        # if the first character is higher than 2, flag it as deleted
                        if user_points[7] in '3456789':
                            too_big_points = False
                    
                    # cut last character
                    user_points = user_points[0:-1]
                    # update points counter
                    if len(user_points) >= 8: points = user_points[7]
                else:
                    # if the user is typing digits
                    if event.key in all_digits:
                        # checks if the user types correctly (after the 7 spaces)
                        if len(user_points) <= 8:
                            # if we're on the first digit cell
                            if len(user_points) == 7:
                                # if the first digit is higher than 2, flag it
                                if event.key in big_digits:
                                    too_big_points = True
                                # type pressed digit
                                user_points += event.unicode
                                # update points counter
                                points = user_points[7]
                                
                            # if we're on the second digit cell
                            else:
                                # if the first digit is exclusively either 1 or 2
                                if too_big_points == False:
                                    # add to points counter
                                    points = user_points[7]
                                    # if the first digit is 2 the user isn't allowed to press a key higher than 6
                                    # max points 26
                                    if user_points[7] == '2' and event.key != pygame.K_7 and event.key != pygame.K_8 and event.key != pygame.K_9:
                                        user_points += event.unicode
                                        points = 10 * int(user_points[7]) + int(user_points[8])
                                    else:
                                        # if the first digit is 1 then do whatever
                                        if user_points[7] == '1':
                                            user_points += event.unicode
                                            points = 10 * int(user_points[7]) + int(user_points[8])

    # Screen Printing
    
    # Display black background
    screen.fill((0,0,0))
    
    # Border Color Flicker
    
    # User Points field border coloring for OnClick
    if user_points_border:
        user_points_color = color_active
    else:
        user_points_color = color_passive
    
    # Submit button border coloring for OnClick
    if submit_button_border and submit_button_press_timer <= 6:
        submit_button_color = color_active
        submit_button_press_timer += 1
    else:
        submit_button_color = color_passive
        submit_button_press_timer = 7
        
    # Score button border coloring for OnClick
    if score_border and score_button_press_timer <= 6:
        score_button_color = color_active
        score_button_press_timer += 1
    else:
        score_button_color = color_passive
        score_button_press_timer = 7
        
    # Reset button border coloring for OnClick
    if reset_border and reset_button_press_timer <= 6:
        reset_button_color = color_active
        reset_button_press_timer += 1
    else:
        reset_button_color = color_passive
        reset_button_press_timer = 7
    
    
    # Draw Labels
    
    # Draw Text Boxes
    pygame.draw.rect(screen, user_points_color, user_points_rect, 2)
    pygame.draw.rect(screen, submit_button_color, submit_button_rect, 2)
    pygame.draw.rect(screen, score_button_color, score_rect, 2)
    pygame.draw.rect(screen, reset_button_color, reset_rect, 2)
    
    # Draw Text
    title_surface = base_font.render(label_title, True, (255, 255, 255))
    credits_surface = credits_font.render(label_credits, True, (255, 255, 255))
    score_surface = base_font.render(label_score, True, (255, 255, 255))
    reset_surface = base_font.render(label_reset, True, (255, 255, 255))
    label_points_surface = base_font.render(label_points, True, (255, 255, 255))
    user_points_surface = base_font.render(user_points, True, (255, 255, 255))
    label_pass_surface = base_font.render(label_pass, True, (255, 255, 255))
    label_datetime_surface = base_font.render(label_datetime, True, (255, 255, 255))
    user_date_surface = base_font.render(user_date, True, (255, 255, 255))
    user_time_surface = base_font.render(user_time, True, (255, 255, 255))
    submit_button_surface = base_font.render(submit_button, True, (255, 255, 255))
    label_version_surface = credits_font.render(label_version, True, (255, 255, 255))
    
    # Print to screen
    screen.blit(title_surface, title_rect)
    screen.blit(credits_surface, credits_rect)
    screen.blit(score_surface,  (score_rect.x + 5, score_rect.y + 5))
    screen.blit(reset_surface,  (reset_rect.x + 5, reset_rect.y + 5))
    screen.blit(label_points_surface, label_points_rect)
    screen.blit(user_points_surface, (user_points_rect.x + 10, user_points_rect.y + 10))
    screen.blit(label_pass_surface, label_pass_rect)
    if int(points) >= 22: screen.blit(check_sprite, check_sprite_rect)
    else: screen.blit(cross_sprite, cross_sprite_rect)
    screen.blit(label_datetime_surface, label_datetime_rect)
    screen.blit(user_date_surface, user_date_rect)
    screen.blit(user_time_surface, user_time_rect)
    screen.blit(submit_button_surface,  (submit_button_rect.x + 42, submit_button_rect.y + 10))
    screen.blit(label_version_surface, label_version_rect)
    
    # Refresh Screen
    pygame.display.flip()
    
    # Tick FPS
    clock.tick(60)