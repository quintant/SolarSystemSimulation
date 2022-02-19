from math import cos, log, pi, sin, sqrt, atan2
from random import randint, uniform
import numpy as np
import pygame

class Planet:
    def __init__(self, mass=1, velocity=None, pos=None, color=None, width=0, height=0, ID=0) -> None:
        # self.screen = screen
        self.mass = mass
        self.ID = ID
        # midx = width/2
        # midy = height/2
        v = 1
        self.velocity = [uniform(-v, v), uniform(-v, v)] if velocity is None else velocity
        x = 500
        self.pos = [randint(0, width), randint(0, height)] if pos is None else pos
        self.color = [randint(100,255), randint(100,255), randint(100,255)] if color is None else color
        if ID==-1: self.color = (150,150,50)
        self.G = 6.67408 * 10e-5  # 6.67408 * 10e-11
        self.delete = False
    
    def __add__(self, other:"Planet"):
        if self.delete or other.delete: return
        # ydiff = other.pos[1] - self.pos[1]
        # xdiff = other.pos[0] - self.pos[0]
        diff = np.subtract(other.pos, self.pos)

        # radius2 = ydiff**2 + xdiff**2
        radius2 = diff[0]**2 + diff[1]**2
        if radius2 < 1e-14: radius2 = 1e-14
        if sqrt(radius2) <= log(pi * pow(self.mass, 2)) + log(pi * pow(other.mass, 2)):
            # other.mass = 0
            if self.mass>=other.mass:
                self.mass +=other.mass
                other.delete = True
            else:
                other.mass += self.mass
                self.delete
                
            # self.velocity = [x + y for x, y in zip(self.velocity, other.velocity)]

        # theta = atan2(ydiff, xdiff)
        theta = np.arctan2(diff[1], diff[0])
        F = self.G * (self.mass * other.mass) / radius2
        velChange = [F*np.cos(theta), F*np.sin(theta)]
        self.velocity = [x + y for x, y in zip(velChange, self.velocity)]

        # other.velocity = [-x + y for x, y in zip(velChange, other.velocity)]
        # other.velChange.append([-x for x in velChange])
        # self.color = [randint(0,255), randint(0,255), randint(0,255)]
