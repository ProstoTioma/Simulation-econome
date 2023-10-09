import random
import time
import math

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

        self.teacher_size = 10
        self.student_size = 2

    def create_population(self, n, new_teachers=False):
        if new_teachers:
            for i in range(n):
                teacher = Entity(0, (200, 200, 200), random.randint(1, 3),
                                              random.randint(0, 800), random.randint(0, 800), is_student=False)
                teacher.x = random.randint(0, self.screenSize)
                teacher.y = random.randint(0, self.screenSize)
                is_touching = self.touch(teacher, self.population)
                at_border = self.border(teacher)

                while is_touching or at_border:
                    teacher.x = random.randint(0, self.screenSize)
                    teacher.y = random.randint(0, self.screenSize)
                    is_touching = self.touch(teacher, self.population)
                    at_border = self.border(teacher)

                self.population.append(teacher)

                self.teachers.append(teacher)



        '''else:
            for i in range(n):
                student = Entity(0, random.choice(self.colours), random.randint(1, 3),
                                              random.randint(0, 800), random.randint(0, 800),
                                              [random.randint(-1, 1), random.randint(-1, 1)])

                self.population.append(student)
                self.students.append(student)
                i += 1
'''
    def run(self):
        self.create_population(100, new_teachers=True)
        stop = False
        while not stop:
            dt = self.clock.tick(60)

            pygame.display.update()
            self.screen.screen.fill((100, 100, 100))
            #print(round(self.years_passed // dt))
            #print(len(self.students))

            # Student-to-Teacher Transition
            for student in self.students:
                if student.age > 13:
                    if random.random() < self.teacher_conversion_rate or student.is_studying:
                        student.is_studying = True
                        if student.age > 19:
                            if random.random() < self.teacher_completion_rate:
                                student.is_student = False
                                self.teachers.append(student)
                                self.students.remove(student)
                                self.create_population(1, new_teachers=True)

                    else:
                        student.alive = False  # Didn't complete teacher training

            self.years_passed += (1 / dt)





            for i in range(len(self.population)):
                if self.population[i].alive:
                    pygame.draw.circle(self.screen.screen, self.population[i].colour,
                                       (self.population[i].x, self.population[i].y), self.teacher_size)
                    self.population[i].live(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop = True
                    break

    def touch(self, entity, population):
        if population:
            for pop in population:
                if (math.sqrt((entity.x - pop.x)**2 + (entity.y - pop.y)**2)) \
                        < (self.teacher_size * 2 + self.student_size * 4.4):
                    return True
        else:
            return False
        return False

    def border(self, entity):
        if entity.x < (self.teacher_size * 2 + self.student_size * 4.4)\
                or entity.y < (self.teacher_size * 2 + self.student_size * 4.4)\
                or entity.x > self.screenSize - (self.teacher_size * 2 + self.student_size * 4.4)\
                or entity.y > self.screenSize - (self.teacher_size * 2 + self.student_size * 4.4):
            return True
        return False







