import torch
from torch import nn
import numpy as np
import pygame as pg

class Model(nn.Module):

    def __init__(self, input_shp):

        super (Model, self).__init__()
        self.Nnet = torch.nn.ModuleList()

        self.k_size = 3
        self.stride = 1
        self.padding = 0
        self.outc = 4
        self.inc = 3 #The number of needs + distance
        self.midc = 8 #m
        self.numLayers = 3


        self.Nnet.append(nn.Linear(self.inc, self.midc))
        self.Nnet.append(nn.ReLU)

        for i in range(self.numLayers):
            self.Nnet.append(nn.Linear(self.midc, self.midc))
            self.Nnet.append(nn.ReLU())

        self.Nnet.append(nn.Linear(self.midc, self.outc))

        self.Nnet.weight = nn.Parameter(
            torch.randn((self.outc, self.inc, self.k_size)),
            requires_grad=False
        )
        self.Nnet.bias = nn.Parameter(
            torch.randn((self.outc,)),
            requires_grad=False
        )


    def forward(self, x):

        x = (x - self.mean) / self.std

        x = self.Nnet(x)

        return x