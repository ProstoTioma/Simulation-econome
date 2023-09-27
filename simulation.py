import random
import time

from screen import Screen
import pygame
from entity import Entity
import random


class Simulation:
    def __init__(self):
        self.screenSize = 800
        self.screen = Screen(self.screenSize, self.screenSize)
        self.population = []
        self.colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
        self.clock = pygame.time.Clock()
        self.dead_count = 0

        self.students = []
        self.teachers = []

        self.teacher_conversion_rate = 0.09  # 9% of students want to become teachers
        self.teacher_completion_rate = 0.60  # 60% of students become teachers
        self.years_passed = 0

    def create_population(self, n, new_teachers=False):

        if new_teachers:
            self.population.append(Entity(0, (200, 200, 200), random.randint(1, 3),
                                          random.randint(0, 800), random.randint(0, 800),
                                          [random.randint(-1, 1), random.randint(-1, 1)], is_student=False))



        else:
            for i in range(n):
                self.population.append(Entity(0, random.choice(self.colours), random.randint(1, 3),
                                              random.randint(0, 800), random.randint(0, 800),
                                              [random.randint(-1, 1), random.randint(-1, 1)]))
                i += 1

    def run(self):
        self.create_population(1000)
        stop = False
        while not stop:
            dt = self.clock.tick(60)

            pygame.display.update()
            self.screen.screen.fill((100, 100, 100))
            print(self.years_passed // dt)

            # Student-to-Teacher Transition
            for student in self.students:
                if student.age > 12:
                    if random.random() < self.teacher_conversion_rate or student.is_studying:
                        student.is_studying = True
                        if student.age > 16:
                            if random.random() < self.teacher_completion_rate:
                                student.is_student = False
                                self.teachers.append(student)
                                self.create_population(1, new_teachers=True)

                    else:
                        student.alive = False  # Didn't complete teacher training

            self.years_passed += (1 / dt)



            for i in range(len(self.population)):
                if self.population[i].alive:
                    pygame.draw.circle(self.screen.screen, self.population[i].colour,
                                       (self.population[i].x, self.population[i].y), 1)
                    self.population[i].live(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop = True
                    break
