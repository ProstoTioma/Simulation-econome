import time
import random


class Entity:
    def __init__(self, age, colour, speed, x, y, move, is_studying=False, is_student=True):
        self.age = age
        self.colour = colour
        self.speed = speed
        self.x = x
        self.y = y
        self.move = move
        self.alive = True
        self.deathAge = random.uniform(1, 2) * 60
        self.is_student = is_student
        self.is_studying = is_studying

    def live(self, dt):
        self.age += 1 / dt
        self.x += self.move[0] * self.speed
        self.y += self.move[1] * self.speed


        if self.age > 20:
            self.alive = False

