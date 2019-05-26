
import pygame as pg
import numpy as np
from GameSettings import *

class Agent(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self, game, startX, startY, AgentI):
        self.map = np.zeros((8,8))
        self.isTurn = True
        self.groups = game.agents
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2)) # The Ones are for aesthetics
        self.image.fill(PlayerColours[AgentI])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

        # Agent Starting Coordinates
        self.x = startX
        self.startX = startX
        self.y = startY
        self.startY = startY
        # Agent Starting Parameters

        self.AgentI = AgentI



        self.maxValue = 100
        self.Hp, self.Hunger, self.Thirst = (self.maxValue,)*3
        self.HungerL = 1
        self.ThirstL = 2


        self.BNeeds = np.array((self.Hunger, self.Thirst))
        self.BNLoss = np.array((self.HungerL, self.ThirstL))

    def respawn(self):
        self.Hp, self.Hunger, self.Thirst = (self.maxValue,) * 3
        self.BNeeds = (self.Hunger, self.Thirst)
        self.x, self.y = self.startX, self.startY

    # Checks to see if a player is in a resource and if so will do the logic for it
    def in_resource(self):
        for resource in self.game.resources:
            if resource.x == self.x and resource.y == self.y and \
                    self.BNeeds[resource.index] + resource.Potency <= self.maxValue:

                self.BNeeds[resource.index] += resource.Potency
                resource.CurrentAmount -= resource.Potency
                resource.turnUpdate()


    # Movement Logic
    def move(self, dx=0, dy=0):
            self.x += dx
            self.y += dy

            self.BNeeds = self.BNeeds - self.BNLoss

            self.BNeeds = np.clip(self.BNeeds, 0, self.maxValue) #Sets min and max values currently replacing death

            # Grid Restrictions
            if self.x > 8 or self.x < 0:
                self.x += -1 * dx
            if self.y > 8 or self.y < 0:
                self.y += -1 * dy
            self.isTurn = False


    # Updates the Needs of the player for printing (May Delete Later)
    def updatestats(self):
        self.Hunger = self.BNeeds[0]
        self.Thirst = self.BNeeds[1]

        for i in self.BNeeds:
            if self.Hp == 0:
                self.respawn()
            elif i < 30:
                self.Hp += -1
            elif i > 70 and self.Hp < 100:
                self.Hp += 1

        print("Agent ", self.AgentI, self.BNeeds, self.Hp)

    # Updates that will happen at every frame
    def update(self):
        self.rect.x = self.x * TILESIZE + TILESIZE/4 # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + TILESIZE/4 # The last additions are for aesthetics


    # Updates that will happen every time a player moves
    def turnUpdate(self, dx=0, dy=0):
        self.move(dx, dy)
        self.in_resource()
        self.updatestats()

