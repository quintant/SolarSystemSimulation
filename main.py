import threading
from spaceManager import SpaceManager
import pygame
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255, 255, 0)
white = (255,255,255)
def main():
    
    pygame.init()
    pygame.display.set_caption("Solar System Sim")

    clock = pygame.time.Clock()
    fps_limit = 30

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = pygame.display.get_surface().get_size()
    
    # Yep, last time I checked the program should be running.
    running = True

    space_manager = SpaceManager(300,  sun=True, width=width, height=height)
    space_manager.start_simulation(screen=screen)
    t = threading.Thread(target=draw)
    t.daemon = True
    t.start()
     
    # main loop
    while running:
        clock.tick(fps_limit)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                space_manager.end_simulation()
                running = False
            # if event.type == pygame.MOUSEBUTTONUP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                space_manager.add(pos)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        space_manager.end_simulation()
                        running = False
                        



def draw():
    while True:
        with threading.Lock():
            pygame.display.update()
        # sleep(0)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()