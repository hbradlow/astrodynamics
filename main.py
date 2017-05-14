#!/usr/bin/env python

from objects import Planet, Satellite

import random, math, pygame
from pygame.locals import *
import pygame.draw

import numpy as np

#constants
WINSIZE = [640, 480]
WINCENTER = [320, 240]

def main():
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Astrodynamics')
    white = 255, 240, 200
    black = 20, 20, 40
    screen.fill(black)

    planet = Planet(30, np.array(WINCENTER), np.array(WINCENTER, dtype=np.float64))
    satellite = Satellite(np.array([150,150], dtype=np.float64), 
                            np.array([0, 100], dtype=np.float64),
                            planet,
                            np.array(WINCENTER, dtype=np.float64)) 

    #main game loop
    done = 0
    while not done:
        screen.fill(black)

        satellite.update(clock.get_time()/1000.0)

        planet.draw(screen)
        satellite.draw(screen)
        satellite.draw_path(screen, white)

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            elif e.type == KEYUP and e.key == K_LEFT:
                satellite.burn(25)
            elif e.type == KEYUP and e.key == K_RIGHT:
                satellite.burn(-25)
            elif e.type == KEYUP and e.key == K_EQUALS:
                satellite.scale *= 1.1
                planet.scale *= 1.1
            elif e.type == KEYUP and e.key == K_MINUS:
                satellite.scale *= 0.9
                planet.scale *= 0.9
        clock.tick(100)


# if python says run, then we should run
if __name__ == '__main__':
    main()
