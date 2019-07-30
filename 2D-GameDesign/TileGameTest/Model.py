import torch
from torch import nn
import numpy as np
import pygame as pg

class Model(nn.Module):

    def __init__(self, input_shp):

        super (Model, self).__init__()

        self.Nnet = torch.nn.ModuleList()

        self.k_size = 3
        self.outchannels = 4 #Up Down Left and Right
        self.inchannels = input_shp[2] #The number of needs + distance

        self.Nnet.append(nn.Conv2d(self.inchannels, 8, self.k_size, padding=1))
        self.Nnet.append(nn.ReLU())
        self.Nnet.append(nn.Conv2d(8, 32, self.k_size))
        self.Nnet.append(nn.ReLU())
        self.Nnet.append(nn.Conv2d(32, 128, self.k_size))
        self.Nnet.append(nn.ReLU())

        self.FC = torch.nn.ModuleList()
        self.FC.append(nn.Linear(3200, 512))
        self.FC.append(nn.ReLU())
        self.FC.append(nn.Linear(512, self.outchannels))



    def forward(self, x):

        x = x.reshape(1, x.shape[2], x.shape[0], x.shape[1])
        # x should already be normalized
        for i in range(6):
            x = self.Nnet[i](x)
        x = torch.flatten(x)

        for i in range(3):
            x = self.FC[i](x)

        return x