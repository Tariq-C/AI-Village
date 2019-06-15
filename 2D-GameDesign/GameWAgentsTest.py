#Credit @KidsCanCode https://www.youtube.com/watch?v=Eltz-XJMxuU&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=2
# Tutorial Followed to create pygame template

# This is the starting code for a new game
import torch
import pygame as pg
import random as rdma


# Constants for the game screen

WIDTH = 720
HEIGHT = 720
FPS = 60

# Colour Definitions

WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

Colours = (RED, BLUE, GREEN, MAGENTA, CYAN, YELLOW)

class Agent(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(Colours[0])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

pg.init()   # initializes Pygame
screen = pg.display.set_mode((WIDTH, HEIGHT)) #Game Window

pg.display.set_caption("This Is A Test Game")   #Sets the title on Game Window
clock = pg.time.Clock() #Game Clock

all_agents = pg.sprite.Group()
agent = Agent()
all_agents.add(agent)
# Game Loop
running = True

while running:
    #keep game running at our defined FPS
    clock.tick(FPS)
    #Process input(events)
    for event in pg.event.get(): #All events are stored in pg.event
        if event.type == pg.QUIT: #pg.QUIT == red x on top right of screen
            running = False
    #Update
    all_agents.update()
    #Display
    screen.fill(BLACK)
    all_agents.draw(screen)
    pg.display.flip() #Make sure to do this after Double buffer