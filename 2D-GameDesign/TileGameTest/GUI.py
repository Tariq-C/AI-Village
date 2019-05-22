import pygame as pg
from GameSettings import *

class GUI(pg.sprite.Sprite):
    #sprite for agents
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        pg.font.init()
        self.game = game

        self.HP = 0
        self.Hunger = 0
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        self.font = pg.font.Font(None, 32)

        # create a text suface object,
        # on which text is drawn on it.
        self.HealthLabel = self.font.render('Health', True, WHITE)
        #self.Health = self.font.render(self.HP, True, WHITE)

        # create a rectangular object for the
        # text surface object
        self.HealthLabelRect = self.HealthLabel.get_rect()
        #self.HealthRect = self.Health.get_rect()

        # set the center of the rectangular object.
        self.HealthLabelRect.center = (WIDTH - GUIX/2, HEIGHT - GUIY/2)




    def update(self, agent):
        self.HP = agent.HP
        self.Hunger = agent.Hunger
        pass