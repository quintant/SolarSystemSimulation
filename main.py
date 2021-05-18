# import the pygame module, so you can use it
from spaceManager import SpaceManager
from planet import Planet
import pygame
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255, 255, 0)
white = (255,255,255)
# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Solar System Sim")

    # clock = pygame.time.Clock()
    # fps_limit = 60
    # create a surface on screen
    height = width = 1000
    mx = my = height // 2
    screen = pygame.display.set_mode((height, width))
     
    # define a variable to control the main loop
    running = True

    space_manager = SpaceManager(300,  sun=True)
     
    # main loop
    while running:
        # clock.tick(fps_limit)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                space_manager.add(pos)
        screen.fill(black)

        space_manager.iterate(screen)

        pygame.display.update()

     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()