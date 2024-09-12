from spaceManager import SpaceManager
import pygame
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255, 255, 0)
white = (255,255,255)

def iterate(space_manager, screen):
    return space_manager.iterate(screen)


def main():
    
    cnt = -1
    pygame.init()
    pygame.display.set_caption("Solar System Sim")


    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()
    
    # Yep, last time I checked the program should be running.
    running = True
    NUM_OBJECTS = 10_000
    space_manager = SpaceManager(NUM_OBJECTS, width=width, height=height)
     
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                import random


        iterate(space_manager, screen)

        pygame.display.flip()
        pygame.image.save(screen, f"gif/{(cnt := cnt + 1)}.png")

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()