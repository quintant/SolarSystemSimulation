import numpy as np
import pygame
import torch
from pygame import surfarray

ATTRACT_RADIUS = 50

class SpaceManager:

    def __init__(self, numObjects, sun=False, width:int=0, height:int=0) -> None:
        self.numObjects = numObjects
        self.width = width
        self.height = height
        self.sun = sun

        self.obj_pos = np.random.uniform(-.5, .5, (self.numObjects, 2)) * np.array([[self.width, self.height]]) / 2 + np.array([[self.width, self.height]]) / 2
        self.obj_pos = torch.tensor(self.obj_pos, dtype=torch.float32, device='cpu', requires_grad=False)

        self.obj_vel = np.random.randn(self.numObjects, 2) * .01
        self.obj_vel = torch.tensor(self.obj_vel, dtype=torch.float32, device='cpu', requires_grad=False)

        self.obj_mass = np.random.randn(self.numObjects) * 100 
        self.obj_mass = torch.tensor(self.obj_mass, dtype=torch.float32, device='cpu', requires_grad=False)

        self.obj_mass[0] = 10_000
        self.mid = np.array([[self.width, self.height]]) / 2
        self.mid = torch.tensor(self.mid, dtype=torch.float32, device='cpu', requires_grad=False)

        self.Z = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.surf = pygame.surfarray.make_surface(self.Z)

        self.n0 = np.zeros(3)
        self.n1 = np.ones(3) * 255

    def iterate2(self, screen):
        old_pos = self.obj_pos.to(torch.int32)
        for i in range(self.numObjects):
            diff = self.obj_pos - self.obj_pos[i]
            dist = torch.sqrt(torch.sum(diff**2, axis=1))
            dist[i] = 1
            # force = (1e-3) * diff * self.obj_mass[i] * self.obj_mass[:, np.newaxis] / dist[:, np.newaxis]**2
            force = (1e-3) * diff * self.obj_mass[:, np.newaxis] / dist[:, np.newaxis]**2
            self.obj_vel[i] += torch.sum(force, axis=0)
        
        self.obj_pos += self.obj_vel
        self.obj_pos[0] = self.mid

        
        DD = self.obj_pos.to(torch.int32)
        for i in range(self.numObjects):
            x, y = old_pos[i]
            if not (x < 0 or x >= self.width or y < 0 or y >= self.height):
                self.Z[x,y] = self.n0
            x, y = DD[i]
            if not (x < 0 or x >= self.width or y < 0 or y >= self.height):
                self.Z[x, y] = self.n1

        surfarray.blit_array(screen, self.Z)
        # for i in range(self.numObjects):
        #     r=1
        #     if i == 0:
        #         r = 10
        #     pygame.draw.circle(
        #         screen,
        #         (0,0,0),
        #         old_pos[i].cpu().numpy().astype(int),
        #         r
        #     )
        #     pygame.draw.circle(
        #         screen,
        #         (255,255,255),
        #         self.obj_pos[i].cpu().numpy().astype(int),
        #         r
        #     )
        # print(np.stack((old_pos, self.obj_pos)).shape)
        # exit()
        # return self.obj_pos
        # return np.stack((old_pos, self.obj_pos))
