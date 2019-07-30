import torch
from torch import optim
import torch.nn as nn
import pygame as pg
import numpy as np
import random as rdm
from GameSettings import *
from Model import *


class Agent(pg.sprite.Sprite):
    # sprite for agents
    def __init__(self, game, startX, startY, AgentI):
        torch.autograd.set_detect_anomaly(True)

        self.isTurn = True

        self.groups = game.agents

        pg.sprite.Sprite.__init__(self)

        self.game = game

        self.image = pg.Surface((TILESIZE / 2, TILESIZE / 2))  # The Ones are for aesthetics
        self.image.fill(PlayerColours[AgentI])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # Agent Starting Coordinates
        self.x = startX
        self.startX = startX
        self.y = startY
        self.startY = startY

        # Agent Internal Map

        self.map = torch.ones(self.game.trainInterval, 9, 9,
                              NUMRESOURCES + 2, requires_grad=False)
        # The goal is to have the total number of resources, the number of agents, and one more for movement
        self.model = Model(self.map[0].shape)
        self.model.train()

        # Create Optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=LEARNINGRATE)

        # Agent Starting Parameters

        self.AgentI = AgentI

        self.maxValue = rdm.randint(100, 300)  # Values wanted is 300
        self.Hp = self.maxValue
        self.TotalReward = 0
        self.TurnReward = 0
        self.LastTurnReward = 0
        self.social = rdm.randint(5,25)

        self.BNeeds = np.ones(NUMRESOURCES + 1)
        self.BNLoss = np.ones(NUMRESOURCES + 1)

        self.TurnLoss = torch.zeros(1, requires_grad=True)
        self.TurnCount = 0

        for i in range(NUMRESOURCES + 1):
            self.BNeeds[i] = self.maxValue
            self.BNLoss[i] = rdm.randint(1, 3)

    def updateMap(self):

        # TODO: Look for a better way to write this code... this is extremely computationally complex for updating an
        #  internal map TODO: Make it so the map only updates a 5x5 around the player. The rest stays the same as the
        #   sight of the agent isn't the whole map Does this need to be done at every move? If this is too
        #   computationally complex, only the step counter will become radial, the rest will only have single values

        self.map = torch.zeros(self.game.trainInterval, 9, 9,
                              NUMRESOURCES + 2, requires_grad=False)

        for i in range(9):
            for j in range(9):
                # First Map is movement
                self.map[self.TurnCount-1][j][i][0] = 0.1#(18 - (abs((i - self.x)) + abs((j - self.y))))/18
        # The next maps are all the resource maps create a radial

        for agent in self.game.agents:
            for i in range(3):
                for j in range(3):
                    x = agent.x + i - 1
                    y = agent.y + j - 1
                    if 0 <= x <= 8 and 0 <= y <= 8:
                        self.map[self.TurnCount-1][y][x][1] += agent.social

        for resource in self.game.resources:
            self.map[self.TurnCount-1][resource.y][resource.x][resource.index+2] = abs(self.BNeeds[resource.index] - self.maxValue)
            #for i in range(9):
             #   for j in range(9):
                    # This makes a radial map of every resource that takes the amount of resource left as a value
              #      self.map[self.TurnCount-1][j][i][1 + resource.index] = (18 - (abs(i - resource.x) + abs(j - resource.y))) \
                                                         #* (1 - (self.BNeeds[resource.index] / self.maxValue)) ** 2

        # To determine location of Agent in all maps
        self.map[self.TurnCount - 1][self.y][self.x][:] = 0
        #print(self.map[:,:,:,0])

    def respawn(self):
        self.Hp = self.maxValue
        for i in range(NUMRESOURCES+1):
            self.BNeeds[i] = self.maxValue
        self.TurnReward = self.TurnReward - 100
        self.x, self.y = self.startX, self.startY

    # Checks to see if a player is in a resource and if so will do the logic for it
    def in_resource(self):
        for resource in self.game.resources:
            if resource.x == self.x and resource.y == self.y and \
                    self.BNeeds[resource.index] + resource.Potency <= self.maxValue:
                self.BNeeds[resource.index] += resource.Potency
                resource.CurrentAmount -= resource.Potency
                resource.turnUpdate()
                self.TurnReward = self.TurnReward + 30

        for agent in self.game.agents:
            if agent.AgentI != self.AgentI:
                if abs(agent.x - self.x) < 2 and abs(agent.y - self.y) < 2:
                    self.BNeeds[-1] += agent.social
                    self.TurnReward = self.TurnReward + 3

    # Movement Logic
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

        self.BNeeds = self.BNeeds - self.BNLoss

        self.BNeeds = np.clip(self.BNeeds, 0, self.maxValue)  # Sets min and max values currently replacing death

        # Grid Restrictions
        if self.x > 8 or self.x < 0:
            self.x += -1 * dx
            self.respawn()
        if self.y > 8 or self.y < 0:
            self.y += -1 * dy
            self.respawn()
        self.isTurn = False

    # Updates the Needs of the player for printing (May Delete Later)
    def updatestats(self):
        for i in self.BNeeds:
            if self.Hp <= 0:
                self.respawn()
            elif i < self.maxValue / 2:
                self.Hp += -1
                self.TurnReward = self.TurnReward + 0
            elif i > self.maxValue / 4 * 3 and self.Hp < self.maxValue:
                self.Hp += 1
                self.TurnReward = self.TurnReward + 0.1
            else:
                self.TurnReward = self.TurnReward + 0.2

        print("Agent ", self.AgentI, self.BNeeds, self.Hp)

    # Updates that will happen at every frame
    def update(self):
        self.rect.x = self.x * TILESIZE + TILESIZE / 4  # The last additions are for aesthetics
        self.rect.y = self.y * TILESIZE + TILESIZE + TILESIZE / 4  # The last additions are for aesthetics

    # Training Segment to adjust the values of the neural network
    def train(self):
        self.optimizer.zero_grad()
        self.TurnLoss = self.TurnLoss + self.TotalReward/self.game.trainInterval
        print(self.TurnLoss, self.TurnReward, self.TotalReward)
        self.TurnLoss.backward()
        self.optimizer.step()
        self.TurnCount = 0
        self.TurnLoss = torch.zeros(1)
        self.TotalReward = 0


    # Updates that will happen every time a player moves
    def turnUpdate(self, dx=0, dy=0):
        self.move(dx, dy)
        if self.TurnCount == self.game.trainInterval:
            self.train()
        self.TurnCount = self.TurnCount + 1
        self.in_resource()
        self.updatestats()
        # This is causing an error to do with inplace operations, but this is the input of the system... why does this happen
        self.updateMap()
        self.TotalReward += self.TurnReward
        self.LastTurnReward = self.TurnReward
        self.TurnReward = 0


    def chooseDirection(self):
        output = self.model.forward(self.map[self.TurnCount-1])

        direction = torch.max(output)
        print(direction)

        self.TurnLoss = self.TurnLoss + (self.TurnReward + direction) / (self.maxValue - self.Hp + 1)

        return output
