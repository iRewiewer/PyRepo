### Libraries ###
import sys, pygame
from pygame.locals import *
from pygame.font import *
from random import random as rng
from msvcrt import getche

from entities import Game, Player, Enemy, Ball

#### This file represents the game itself and all of its modes ####

def game_setup(screen_object, window_size, colors, fonts, gamemode):
    game = Game(screen_object, window_size, colors, fonts, 60, gamemode)
    player = Player(4, 0)
    enemy = Enemy(4, 0)

    if game.gamemode == "singleplayer": ball = Ball(3, 0.3)
    else: ball = Ball(4, 0.3)

    update(game, player, enemy, ball)

def update_scene(game, player, enemy, ball):
    # Update objects' positions
    player.object = player.object.move(100,230)
    ball.object = ball.object.move(500,290)
    enemy.object = enemy.object.move(900,230)

    # User's name input textbox after game end
    game.text_name = game.text_name_font.render("", True, game.text_color, game.text_background_color)
    text_name_object = game.text_name.get_rect()
    text_name_object.center = (310, 260)

    # Define ball's starting velocity based on rng()
    velocity_rng = int(rng() * 100)

    # Down Right v>
    # Takes 6 turns for the player to win (4-4-3) speed
    if velocity_rng % 4 == 0: ball.mode = 0

    # Up Right ^>
    # Takes 16 turns for the player to win (4-4-3) speed
    elif velocity_rng % 4 == 1: ball.mode = 1

    # Down Left <v
    # Takes 69 turns for the player to win (4-4-3) speed
    elif velocity_rng % 4 == 2: ball.mode = 2
        
    # Up Left <^
    # Takes 59 turns for the player to win (4-4-3) speed
    elif velocity_rng % 4 == 3: ball.mode = 3

    else: pass

    # Current game turn - for debug purposes
    # game.turn = 1
    
    # Display start direction in console - for debug purposes
    # print("")
    # if ball.mode == 0: print("Starting ball direction: Down Right (v>)")
    # if ball.mode == 1: print("Starting ball direction: Up Right (^>)")
    # if ball.mode == 2: print("Starting ball direction: Down Left (<v)")
    # if ball.mode == 3: print("Starting ball direction: Up Left (<^)")
    # print("")

def update(game, player, enemy, ball):
    # Happens each time anyone scores
    update_scene(game, player, enemy, ball)

    # The game loop
    while True:

        # FPS tick
        game.clock.tick(game.fps)
        
        # Fill the screen with the selected background color
        game.screen_object.fill(game.text_background_color)
        
        # Array of all keys pressed
        keys_pressed = pygame.key.get_pressed()
        
        # Close application on exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        # Close application on special key combo
        if ((keys_pressed[pygame.K_RALT] or keys_pressed[pygame.K_LALT]) and keys_pressed[pygame.K_F4]) or keys_pressed[pygame.K_ESCAPE]: sys.exit()
          


        ## Paddles Movement

        # Player movement - Up or Down
        elif keys_pressed[pygame.K_w]:
            if not player.object.colliderect(game.hu_object):
                player.object = player.object.move(0, -player.speed)
            
        elif keys_pressed[pygame.K_s]:
            if not player.object.colliderect(game.hd_object):
                player.object = player.object.move(0, player.speed)

        # Enemy movement - ignore if MP is selected
        elif game.gamemode == "multiplayer":
            if keys_pressed[pygame.K_UP]:
                if not enemy.object.colliderect(game.hu_object):
                    enemy.object = enemy.object.move(0, -enemy.speed)
                
            elif keys_pressed[pygame.K_DOWN]:
                if not enemy.object.colliderect(game.hd_object):
                    enemy.object = enemy.object.move(0, enemy.speed)
            else:
                pass
        else:
            pass
        


        ## Ball Movement

        # Ball collision with left wall
        if ball.object.colliderect(game.vl_object):
            # If endless mode is on, end the game
            if game.gamemode == "endless": game.isEndgame = True
            enemy.score += 1
            break
            
        # Ball collision with right wall
        if ball.object.colliderect(game.vr_object):
            player.score += 1
            #break
            
        # Game over conditions
        if player.score == 7 or enemy.score == 7 and game.gamemode != "endless":
            game.isEndgame = True
            break

        if ball.mode == 0: # Down Right v>
            if ball.object.colliderect(game.hd_object):
                # If it collides with a wall (up/down) change direction
                ball.mode = 1

            elif ball.object.colliderect(enemy.object):
                # Debug variables
                # print("Turn: " + str(turn))
                # print(ball.speed)
                # game.turn += 1

                # If it collides with the enemy paddle change direction
                ball.mode = 2
                
                # Increase ball factor speed for multiplayer
                if game.gamemode == "multiplayer": ball.speed += ball.incremental_factor     
                
                # If playing endless, add a point to the player
                if game.gamemode == "endless": player.score += 1

            else:
                ball.object = ball.object.move(ball.speed, ball.speed)
                if game.gamemode == "singleplayer" or game.gamemode == "endless": enemy.object = enemy.object.move(0, enemy.speed)
            
        elif ball.mode == 1: # Up Right ^>
            if ball.object.colliderect(game.hu_object):
                # If it collides with a wall (up/down) change direction
                ball.mode = 0

            if ball.object.colliderect(enemy.object):
                # Debug variables
                # print("Turn: " + str(turn))
                # print(ball.speed)
                # game.turn += 1

                # If it collides with the enemy paddle change direction
                ball.mode = 3
                
                # Increase ball factor speed for multiplayer
                if game.gamemode == "multiplayer": ball.speed += ball.incremental_factor
                
                # If playing endless, add a point to the player
                if game.gamemode == "endless": player.score += 1
                
            else:
                ball.object = ball.object.move(ball.speed, -ball.speed)
                if game.gamemode == "singleplayer" or game.gamemode == "endless": enemy.object = enemy.object.move(0, -enemy.speed)
            
        elif ball.mode == 2: # Down Left <v
            if ball.object.colliderect(game.hd_object): 
                 # If it collides with a wall (up/down) change direction
                ball.mode = 3

            if ball.object.colliderect(player.object):
                # Debug variables
                # print("Turn: " + str(turn))
                # print(ball.speed)
                # game.turn += 1

                # If it collides with the enemy paddle change direction
                ball.mode = 0
                
                # Increase ball factor speed for multiplayer
                if game.gamemode == "multiplayer": ball.speed += ball.incremental_factor
                
            else:
                ball.object = ball.object.move(-ball.speed, ball.speed)
                if game.gamemode == "singleplayer" or game.gamemode == "endless": enemy.object = enemy.object.move(0, enemy.speed)      
            
        else: # When ball.mode == 3 - Up Left <^ 
            if ball.object.colliderect(game.hu_object):
                 # If it collides with a wall (up/down) change direction
                ball.mode = 2

            if ball.object.colliderect(player.object):
                # Debug variables
                # print("Turn: " + str(turn))
                # print(ball.speed)
                # game.turn += 1

                # If it collides with the enemy paddle change direction
                ball.mode = 1
                
                # Increase ball factor speed for multiplayer
                if game.gamemode == "multiplayer": ball.speed += ball.incremental_factor
                
            else:
                ball.object = ball.object.move(-ball.speed, -ball.speed)
                if game.gamemode == "singleplayer" or game.gamemode == "endless": enemy.object = enemy.object.move(0, -enemy.speed)
                


        ## Score System
        
        # Display player score
        player.score_display = game.score_font.render(str(player.score), True, game.text_color, game.text_background_color)
        player.score_display_object = player.score_display.get_rect()
        player.score_display_object.center = (game.window_size[0] // 2 - 200, 75)

        # Display enemy score
        enemy.score_display = game.score_font.render(str(enemy.score), True, game.text_color, game.text_background_color)
        enemy.score_display_object = enemy.score_display.get_rect()
        enemy.score_display_object.center = (game.window_size[0] // 2 + 200, 75)
        
        # Render UI Elements - separator, score displays
        game.screen_object.blit(game.separator_sprite, game.separator_object)
        game.screen_object.blit(player.score_display, player.score_display_object)
        if game.gamemode != "endless": # If not playing endless
            game.screen_object.blit(enemy.score_display, enemy.score_display_object)
        
        # Render entities
        game.screen_object.blit(player.sprite, player.object)
        game.screen_object.blit(enemy.sprite, enemy.object)
        game.screen_object.blit(ball.sprite, ball.object)
        
        # Render walls
        game.screen_object.blit(game.vl_sprite, game.vl_object)
        game.screen_object.blit(game.vr_sprite, game.vr_object)
        game.screen_object.blit(game.hu_sprite, game.hu_object)
        game.screen_object.blit(game.hd_sprite, game.hd_object)
        
        # Updates entire screen_object
        pygame.display.flip()



    ## Out of game loop, Inside setup loop

    if game.isEndgame == True:
    
        # If not playing endless end the game and return to menu
        if game.gamemode != "endless": pass

        # If playing endless, add the score to the highscore table if it's high enough to qualify
        else: endless_score(game, player.score)


def endless_score(game, score):
    finished = False # Finished writing and pressed enter
    name = "" # Final name
    cell = ["", "", ""] # Name cells
    cell_index = 0 # Current selected cell
    backspace_count = 0 # Number of backspaces issued

    # If the player is in top 10, add them to the leaderboard
    if score >= get_last_score():        
        while not finished:
            for event in pygame.event.get():
                print(str(chr(event.key)))
                if event.type == pygame.KEYDOWN:
                    # If backspace is pressed, delete 1 character if possible
                    if event.key == pygame.K_BACKSPACE:
                        if cell_index != 0: backspace_count += 1
                    
                    # Character of the key pressed
                    event_key = str(chr(event.key))
                    
                    # If the current cell is still within the 3 letters limit
                    if cell_index == 0 or cell_index == 1 or cell_index == 2:
                        if event_key >= 'a' and event_key <= 'z':
                            cell[cell_index] = str( ord(event_key) - 32)
                            cell_index += 1
                            
                        if event_key >= 'A' and event_key <= 'Z':
                            cell[cell_index] = event_key
                            cell_index += 1

                    # If the user presse backspace and it's not the first cell
                    if cell_index != 0 and backspace_count >= 1:
                        backspace_count -= 1
                        cell_index -= 1

                    # If the user pressed enter and the name has been chosen
                    if event.key == 13 and cell_index == 3:
                        finished = True
                        name += cell[0] + cell[1] + cell[2]
                        break # Break for loop
                    
                    # Display text
                    text_name = game.text_name_font.render(name, True, game.text_color, game.text_background_color)
                    text_name_object = text_name.get_rect()
                    
                    # Display name input box
                    game.screen_object.blit(game.name_box, game.name_box_object)
                    game.screen_object.blit(text_name, text_name_object)
                    pygame.display.flip()
                    
                    # Wait for input so the game doesn't freeze
                    x = getche()

            if finished == True: break

        add_highscore(name, score)

def add_highscore(name, score):
    # Read all the highscores from the respective file
    try:
        file = open("highscores.yml", "r")
        
        highscores_list = file.read()
        highscores_list = highscores_list.split("\n")

        for i in range (0, len(highscores_list)):
            highscores_list[i] = highscores_list[i].split(":")

    except:
        raise("Error: Line 359, highscores.py, Error reading highschores from file.")

    finally:
        file.close()
    
    highscores_list.append([name, score])
    highscores_list.sort(key = lambda x: int(x[1]), reverse = True) # Sort in descending order by the second element
    highscores_list.pop()
    
    file = open("highscores.yml", "w")
    for i in range (0, len(highscores_list) - 1): file.write(highscores_list[i][0] + ":" + highscores_list[i][1] + "\n")
    file.close()

def get_last_score():
    # Read all the highscores from the respective file
    try:
        file = open("highscores.yml", "r")
        
        highscores_list = file.read()
        highscores_list = highscores_list.split("\n")

        for i in range (0, len(highscores_list)):
            highscores_list[i] = highscores_list[i].split(":")

    except:
        raise("Error: Line 384, highscores.py, Error reading highschores from file.")

    finally:
        file.close()
    
    return int(highscores_list[11][1])