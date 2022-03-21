from concurrent.futures import ThreadPoolExecutor
from math import log, sqrt, pi
from random import uniform
from typing import List
import numpy as np
import pygame
from planet import Planet
import threading
from time import sleep

from utils import rad

ATTRACT_RADIUS = 100

class SpaceManager:

    def __init__(self, numObjects, sun=False, width:int=0, height:int=0) -> None:
        self.numObjects = numObjects
        self.width = width
        self.height = height
        self.solarSystem: List[Planet] = []
        self.__populate(sun)
        self.garbage: List[Planet] = []
        self.add_queue: List[Planet] = []
        self.cnt = 0
        self._continue_sim = False
        self._sim_thread = None

    
    def __populate(self, sun=False):
        if sun:
            self.solarSystem.append(Planet(ID=0, mass=1e+6, pos=[self.width//2, self.height//2]))
        for i in range(self.numObjects):
            self.solarSystem.append(Planet(ID=i+1 if sun else i, width=self.width, height=self.height))
        
    def add(self, pos, vel=None):
        with threading.Lock():
            v = 2
            self.add_queue.append(Planet(ID=self.numObjects, pos=pos, velocity=vel))
            # self.numObjects += 1

    def start_simulation(self, screen):
        self._continue_sim = True
        self._sim_thread = threading.Thread(target=self.iterate, args=(screen,))
        self._sim_thread.daemon = True
        self._sim_thread.start()
    
    def end_simulation(self):
        self._continue_sim = False
        self._sim_thread.join()

    
    
    def iterate(self, screen):
        while self._continue_sim:
            executor = ThreadPoolExecutor(max_workers=24)
            nparr = np.array([pl.pos for pl in self.solarSystem])
            for planet in self.solarSystem:
                executor.submit(self.__iteration, planet=planet, nparr=nparr)
                # self.__iteration(planet=planet, nparr=nparr)
            executor.shutdown(wait=True)

            with  threading.Lock():
                self.solarSystem.extend(self.add_queue)
                self.add_queue = []

            updated_ID = 0
            for planet in self.solarSystem:
                if planet.delete == True:
                    self.numObjects -= 1
                    self.garbage.append(planet)
                else:
                    planet.ID = updated_ID
                    updated_ID += 1
                    if planet.ID != 0: # Clear the previous position
                        pygame.draw.circle(
                        screen,
                        (0,0,0),
                        planet.pos,
                        rad(planet.mass, norm=True)
                        )
                        # planet.pos = [x+y/planet.mass for x, y in zip(planet.pos, planet.velocity)]
                        planet.pos = planet.pos + planet.velocity
                    
                    pygame.draw.circle(
                        screen,
                        planet.color,
                        planet.pos,
                        rad(planet.mass, norm=True)
                    )
            for planet in self.garbage:
                pygame.draw.circle(
                            screen,
                            (0,0,0),
                            planet.pos,
                            rad(planet.mass, norm=True)
                            )
                self.solarSystem.remove(planet)
            self.garbage = []
            sleep(0.001)

    def __iteration(self, planet: Planet, nparr:np.ndarray):
        if -500 < planet.pos[0] < self.width + 500 or -500 < planet.pos[1] < self.height + 500:
            ndiff = nparr-planet.pos
            nrad2 = (ndiff**2).sum(axis=1)
            for i, p in enumerate(self.solarSystem):
                if i != planet.ID and (nrad2[i] < ATTRACT_RADIUS**2 or i == 0):
                    planet + p
        else:
            planet.delete = True
