import random


class Entity:
    def __init__(self, teacher_id, age, colour, x, y, is_studying=False, is_student=True):
        self.id = teacher_id
        self.age = age
        self.colour = colour
        self.x = x
        self.y = y
        self.alive = True
        self.deathAge = random.uniform(1, 2) * 60
        self.is_student = is_student
        self.is_studying = is_studying
        self.students = []
        self.burnout = 0.023
        self.speed = 1

    def live(self):
        self.age += 1 * self.speed


