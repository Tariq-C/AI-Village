import pygame as pg
from GameSettings import *

class Agent(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self, game, startX, startY):
        self.groups = game.all_agents
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2)) # The Ones are for aesthetics
        self.image.fill(PlayerColours[0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # Agent Starting Coordinates
        self.x = startX
        self.y = startY
        # Agent Starting Parameters

        self.maxHp = 100
        self.Hp = self.maxHp
        self.maxHunger = 100
        self.Hunger = self.maxHunger

    def in_resource(self):
        for resource in self.game.resources:
            if resource.x == self.x and resource.y == self.y:
                self.Hunger += 5
                resource.CurrentFood -= 5

                if self.Hunger > self.maxHunger:
                    self.Hunger = self.maxHunger

    def move(self, dx=0, dy=0):
            self.x += dx
            self.y += dy
            self.Hunger -= 1
            if self.x > 8 or self.x < 0:
                self.x += -1 * dx
            if self.y > 8 or self.y < 0:
                self.y += -1*dy
            print(self.Hunger)


    def update(self):
        self.rect.x = self.x * TILESIZE + TILESIZE/4 # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + TILESIZE/4 # The last additions are for aesthetics
        self.in_resource()