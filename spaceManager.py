from math import log, sqrt, pi
from random import uniform
import pygame
from planet import Planet
import threading

from time import sleep


class SpaceManager:
    def __init__(self, numObjects, sun=False, width:int=0, height:int=0) -> None:
        self.numObjects = numObjects
        self.width = width
        self.height = height
        # self.screen = screen
        self.solarSystem = []
        self.__populate(sun)
        self.garbage = []
        self.cnt = 0
        self._continue_sim = False
        self._sim_thread = None

    
    def __populate(self, sun=False):
        if sun:
            self.solarSystem.append(Planet(ID=-1, mass=1e+6, pos=[self.width//2, self.height//2]))
        for i in range(self.numObjects):
            self.solarSystem.append(Planet(ID=i, width=self.width, height=self.height))
        
    def add(self, pos):
        v = 2
        velocity = [uniform(-v, v), uniform(-v, v)]
        self.numObjects
        self.solarSystem.append(Planet(ID=self.numObjects, pos=pos, velocity=velocity))
        self.numObjects += 1

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
            # with threading.Lock():
            for planet in self.solarSystem:
                self.__iteration(planet=planet)
            
            for planet in self.solarSystem:
                if planet.delete == True:
                    self.numObjects -= 1
                    self.garbage.append(planet)
                else:
                    if planet.ID != -1:
                        pygame.draw.circle(
                        screen,
                        (0,0,0),
                        planet.pos,
                        log(pi * pow(planet.mass, 2))
                        )
                        planet.pos = [x+y/planet.mass for x, y in zip(planet.pos, planet.velocity)]

                    pygame.draw.circle(
                        screen,
                        planet.color,
                        planet.pos,
                        log(pi * pow(planet.mass, 2))
                    )
            for planet in self.garbage:
                pygame.draw.circle(
                            screen,
                            (0,0,0),
                            planet.pos,
                            log(pi * pow(planet.mass, 2))
                            )
                self.solarSystem.remove(planet)
            self.garbage = []
            sleep(0.001)
            # sleep(0)

    def __iteration(self, planet: Planet):
        if -500 < planet.pos[0] < self.width + 500 or -500 < planet.pos[1] < self.height + 500:
            for p in self.solarSystem:
                if p.ID != planet.ID:
                    xdiff = planet.pos[0] - p.pos[0]
                    ydiff = planet.pos[1] - p.pos[1]
                    rad2 = sqrt(xdiff**2 + ydiff**2)
                    if rad2 < 50 or p.ID == -1:
                        planet + p
        else:
            planet.delete = True
