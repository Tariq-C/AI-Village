#Credit @KidsCanCode https://www.youtube.com/watch?v=Eltz-XJMxuU&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=2
# Tutorial Followed to create pygame template

# This is the starting code for a new game

import pygame as pg
import random as rdm
import sys
from GameSettings import *
from Agent import *
from ResourceTile import *
from GUI import *



class Game:
    def __init__(self):
        # Initialize game window
        self.running = True

        pg.init()  # initializes Pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Game Window

        pg.display.set_caption("This Is A Test Game")  # Sets the title on Game Window
        self.clock = pg.time.Clock()  # Game Clock
        self.resourceTileI = 0
        self.agentI = 0


    def run(self):
        # Game Loop
        self.inGame = True
        while self.inGame:
            # Keep game running at our defined FPS
            self.clock.tick(FPS)
            for agent in self.agents:
                agent.isTurn = True
                while agent.isTurn == True:
                    #TODO: Write the Draw UI code
                    self.drawUI(agent)
                    self.turnevents(agent)
                    self.update()
                    self.draw()

    def update(self):
        # Game Loop Update
        self.resources.update()
        self.agents.update()

    def turnevents(self, agent):
        for event in pg.event.get():
            #TODO: Make the quit work on every click not just intermediate ones
            if event.type == pg.QUIT:  # pg.QUIT == red x on top right of screen
                if self.inGame:
                    self.inGame = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    agent.turnUpdate(dy=-1)
                if event.key == pg.K_a:
                    agent.turnUpdate(dx=-1)
                if event.key == pg.K_s:
                    agent.turnUpdate(dy=1)
                if event.key == pg.K_d:
                    agent.turnUpdate(dx=1)

    # Events that take place at every frame
    def events(self):
        # Process input(events)
        for event in pg.event.get():  # All events are stored in pg.event
            for agent in self.agents:
                agent.isTurn = True
                while agent.isTurn == True: #Logic to make it so only one player can make a move at a time
                    self.turnevents(agent)
                    self.update()
                    self.draw()

    # Will draw the UI when completed
    def drawUI(self, agent):
        #TODO: Write this code
        #self.GUI.draw(self.screen, )
        pass

    # Draws the changes in states to the screen
    def draw(self):
        # Game Loop Events

        self.screen.fill(BLACK)
        self.draw_grid()
        self.resources.draw(self.screen)
        self.agents.draw(self.screen)
        pg.display.flip()  # Make sure to do this after Double buffer

    # This is a method used to draw the grid within the simulation
    # Input: None
    # Output: A Grid drawn on the GUI

    def draw_grid(self):
        for x in range(GUIY, WIDTH-GUIX+1, TILESIZE):
            pg.draw.line(self.screen, WHITE, (x, GUIY), (x,HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, WHITE, (0, y), (WIDTH-GUIX, y))

    # This is a method to create a new Agent
    # Input: Takes the x and y position on the grid
    # Output: Adds a new Agents to the group agents
    def newAgent(self,  positionX, positionY):
        self.agents.add(Agent(self, positionX, positionY, self.agentI))
        self.agentI += 1

    # This is a method to create a new Resource Tile
    # Input: Takes the x and y position on the grid
    # Output: Adds a new Resource Tile to the group resources
    def newReourceTile(self, positionX, positionY):
        self.resources.add(ResourceTile(self, positionX, positionY, self.resourceTileI))
        self.resourceTileI += 1

    # This is the method when starting a new game
    def new(self):
        #Starts Game
        self.resources = pg.sprite.Group()
        self.agents = pg.sprite.Group()
        self.GUI = pg.sprite.Group()
        self.gui1 = GUI(self)

        self.newReourceTile(3, 3)
        self.newReourceTile(3, 2)

        self.newAgent(0, 0)
        self.GUI.add(self.gui1)
        self.run()


    def train(self):
        pass



g = Game()

while g.running:
    g.new()

pg.quit()
