import random
import time

from screen import Screen
import pygame
from entity import Entity
import random


class Simulation:
    def __init__(self):
        self.screenSize = 600
        self.screen = Screen(self.screenSize, self.screenSize)
        self.population = []
        self.colours = ['blue', 'yellow', 'green']
        self.clock = pygame.time.Clock()
        self.fd = []
        self.kill_count = 0
        self.dead_count = 0



    def run(self):
        stop = False
        while not stop:
            dt = self.clock.tick(60)
            pygame.display.update()
            self.screen.screen.fill((100, 100, 100))
            for i in range(len(self.population)):
                if self.population[i].alive:
                    pygame.draw.circle(self.screen.screen, self.population[i].colour,
                                       (self.population[i].x, self.population[i].y), 1)
                    self.population[i].live(dt)
                for i in range(len(self.fd)):
                    if self.fd[i].alive:
                        pygame.draw.circle(self.screen.screen, (50, 50, 50), (self.fd[i].x, self.fd[i].y), 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop = True
                    break
