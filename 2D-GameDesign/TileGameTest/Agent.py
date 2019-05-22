import pygame as pg
import numpy as np
from GameSettings import *

class Agent(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self, game, startX, startY, AgentI):
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
        self.y = startY
        # Agent Starting Parameters

        self.AgentI = AgentI

        #TODO: Clean up to take values from resources in the system


        self.maxHp = 100
        self.Hp = self.maxHp
        self.maxHunger = 100
        self.Hunger = self.maxHunger
        self.HungerL = 1
        self.maxThirst = 100
        self.Thirst = self.maxThirst
        self.ThirstL = 2



        self.maxBN = np.array((self.maxHunger, self.maxThirst))
        self.BNeeds = np.array((self.Hunger, self.Thirst))
        self.BNLoss = np.array((self.HungerL, self.ThirstL))



    # Checks to see if a player is in a resource and if so will do the logic for it
    def in_resource(self):
        for resource in self.game.resources:
            if resource.x == self.x and resource.y == self.y:

                self.BNeeds[resource.index] += resource.Potency
                resource.CurrentAmount -= resource.Potency
                resource.turnUpdate()

                if self.BNeeds[resource.index] > self.maxBN[resource.index]:
                    self.BNeeds[resource.index] = self.maxBN[resource.index]


    # Movement Logic
    def move(self, dx=0, dy=0):
            self.x += dx
            self.y += dy


            self.BNeeds = self.BNeeds - self.BNLoss


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
        print("Agent ", self.AgentI, self.Hunger, self.Thirst)

    # Updates that will happen at every frame
    def update(self):
        self.rect.x = self.x * TILESIZE + TILESIZE/4 # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + TILESIZE/4 # The last additions are for aesthetics


    # Updates that will happen every time a player moves
    def turnUpdate(self, dx=0, dy=0):
        self.move(dx, dy)
        self.in_resource()
        self.updatestats()