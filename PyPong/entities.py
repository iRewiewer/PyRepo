### Libraries ###
import pygame
from pygame.font import *

class Game:
    def __init__(self, screen_object, window_size, colors, fonts, fps, gamemode):
        # Utility parameters
        self.screen_object = screen_object
        self.window_size = window_size
        self.gamemode = "singleplayer"
        self.turn = 0

        # Define game fps
        self.clock = pygame.time.Clock()
        self.fps = fps

        # Game over checker
        self.isEndgame = False

        ## Define scene objects

        # vl - vertical left
        self.vl_sprite = pygame.image.load("assets/images/vertical_wall.png")
        self.vl_object = self.vl_sprite.get_rect().move(0, 0)

        # vr - vertical right
        self.vr_sprite = pygame.image.load("assets/images/vertical_wall.png")
        self.vr_object = self.vr_sprite.get_rect().move(999, 0)

        # hu - horizontal up
        self.hu_sprite = pygame.image.load("assets/images/horizontal_wall.png")
        self.hu_object = self.hu_sprite.get_rect().move(0, 0)

        # hd - horizontal down
        self.hd_sprite = pygame.image.load("assets/images/horizontal_wall.png")
        self.hd_object = self.hd_sprite.get_rect().move(0, 599)

        self.separator_sprite = pygame.image.load("assets/images/separator.png")
        self.separator_object = self.separator_sprite.get_rect().move(499, 0)

        self.name_box_sprite = pygame.image.load("assets/images/name_box.png")
        self.name_box_object = self.name_box_sprite.get_rect().move(300, 250)

        # Define object's game.colors
        self.text_color = colors["white"]
        self.text_background_color = colors["black"]

        # Font setup
        self.score_font = Font(fonts["LCD"], 42)
        self.text_name_font = Font(fonts["LCD"], 32)

class Player:
    def __init__(self, speed, score):
        self.speed = speed # default is 4
        self.score = score # default is 0
        self.sprite = pygame.image.load("assets/images/paddle.png")
        self.object = self.sprite.get_rect()

class Enemy:
    def __init__(self, speed, score):
        self.speed = speed # default is 3 for SG, 4 for MP
        self.score = score # default is 0
        self.sprite = pygame.image.load("assets/images/paddle.png")
        self.object = self.sprite.get_rect()

class Ball:
    def __init__(self, speed, incremental_factor):
        self.speed = speed # default is 4
        self.incremental_factor = incremental_factor # default is 0.3
        self.sprite = pygame.image.load("assets/images/ball.png")
        self.object = self.sprite.get_rect()
        self.mode = 0