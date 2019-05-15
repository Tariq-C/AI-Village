import pygame as pg
from GameSettings import *
import random as rdm

class Food(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self, game, startX, startY):
        self.groups = game.all_agents, game.resources
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE-1, TILESIZE-1)) # The Ones are for aesthetics
        self.image.fill(ResourceColours[0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # Agent Starting Coordinates
        self.x = startX
        self.y = startY
        # Agent Starting Parameters
        self.CurrentFood = rdm.randint(30, 50)
        self.MaxFood = self.CurrentFood

    def regrow(self):
        self.x = rdm.randint(0, 8)
        self.y = rdm.randint(0, 8)
        self.CurrentFood = rdm.randint(30, 50)

    def update(self):
        if self.CurrentFood < 0:
            self.regrow()
        self.rect.x = self.x * TILESIZE + 1  # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + 1
        
