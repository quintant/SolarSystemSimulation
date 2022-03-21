from math import cos, log, pi, sin, sqrt, atan2
from random import randint, uniform
import numpy as np
import pygame

from utils import massDist, posDist, rad


class Planet:
    def __init__(
        self, mass=None, velocity=None, pos=None, color=None, width=0, height=0, ID=0
    ) -> None:
        # self.screen = screen
        self.mass = massDist() if mass is None else mass
        self.ID = ID
        v = 2
        self.velocity = (
            np.array([uniform(-v, v), uniform(-v, v)])
            if velocity is None
            else np.array(velocity)
        )
        ppp = uniform(0, 2*pi)
        self.pos: np.ndarray = (
            np.array([posDist(mu = width/2, p=ppp, pf=cos), posDist(mu=height/2, p=ppp, pf=sin)]) if pos is None else pos
        )
        self.color = (
            [randint(100, 255), randint(100, 255), randint(100, 255)]
            if color is None
            else color
        )
        if ID == 0:
            self.color = (150, 150, 50)
        # G = 6.67408 * 10e-5  # 6.67408 * 10e-11
        G = 6.67408 * 10e-8
        self.G = np.array([G, G])
        self.delete = False

    def __add__(self, other: "Planet"):
        if self.delete or other.delete:
            return
        diff = np.subtract(other.pos, self.pos)

        radius2 = np.sqrt((diff**2).sum())
        if radius2 < 1e-14:
            radius2 = 1e-14
        if radius2 <= rad(self.mass, norm=True) + rad(other.mass, norm=True):
            # other.mass = 0
            if self.mass >= other.mass:
                self.mass += other.mass
                other.delete = True
                # else:
                #     other.mass += self.mass
                #     self.delete = True

                # self.velocity = [x + y for x, y in zip(self.velocity, other.velocity)]

                # theta = atan2(ydiff, xdiff)
        theta = np.arctan2(diff[1], diff[0])
        F = self.G * (self.mass * other.mass) / radius2
        velChange = np.array([np.cos(theta), np.sin(theta)]) * F
        self.velocity = velChange + self.velocity
