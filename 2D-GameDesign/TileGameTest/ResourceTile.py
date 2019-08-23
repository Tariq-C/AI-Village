import pygame as pg
from GameSettings import *
import random as rdm


class ResourceTile(pg.sprite.Sprite):
    # sprite for agents
    def __init__(self, game, startX, startY, index):
        self.groups = game.resources
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE - 1, TILESIZE - 1))  # The Ones are for aesthetics
        self.image.fill(ResourceColours[index])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # Agent Starting Coordinates
        self.x = startX
        self.y = startY
        # Agent Starting Parameters
        self.CurrentAmount = 100000 #rdm.randint(600, 900)
        self.Potency = rdm.randint(15, 25)

        self.index = index

    # When out of resource, will appear elsewhere
    def regrow(self):
        self.CurrentAmount = 100000#rdm.randint(60, 90)
        self.Potency = rdm.randint(15, 25)

    # Updates every frame
    def update(self):
        self.rect.x = self.x * TILESIZE + 1  # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + 1

    # Updates to happen when a player moves into the tile
    def turnUpdate(self):
        if self.CurrentAmount < 0:
            self.regrow()
