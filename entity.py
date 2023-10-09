import time
import random


class Entity:
    def __init__(self, age, colour, x, y, is_studying=False, is_student=True):
        self.age = age
        self.colour = colour
        self.x = x
        self.y = y
        self.alive = True
        self.deathAge = random.uniform(1, 2) * 60
        self.is_student = is_student
        self.is_studying = is_studying

    def live(self, dt):
        self.age += 1 / dt



        #if self.age > 20:
        #    self.alive = False

