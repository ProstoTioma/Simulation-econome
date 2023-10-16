import math
import random
import pygame
from screen import Screen
from entity import Entity

class Simulation:
    def __init__(self):
        self.screenSize = 800
        self.colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
        self.clock = pygame.time.Clock()
        self.students = []
        self.teachers = []
        self.dead_count = 0
        self.teacher_conversion_rate = 0.09
        self.teacher_completion_rate = 0.60
        self.years_passed = 0
        self.year = 0
        self.teacher_size = 10
        self.student_size = 2  # Increase student size for visibility
        self.student_spawn_radius = 5  # Maximum distance from the teacher for student spawn
        self.screen = Screen(self.screenSize, self.screenSize)

    def create_entity(self, is_student):
        age = random.randint(25, 35) if not is_student else 0
        color = (200, 200, 200) if not is_student else random.choice(self.colours)
        x, y = random.randint(0, self.screenSize), random.randint(0, self.screenSize)
        entity = Entity(len(self.students) + 1, age, color, x, y, is_student=is_student)
        return entity

    def create_population(self, n, is_student=True):
        population = self.students if is_student else self.teachers
        max_attempts = 100  # Maximum attempts to create non-overlapping entity
        for i in range(n):
            attempts = 0
            while attempts < max_attempts:
                entity = self.create_entity(is_student)
                if is_student:
                    teacher = random.choice(self.teachers)
                    self.spawn_student_near_teacher(entity, teacher)
                if not self.is_entity_overlapping(entity, population) and not self.is_entity_at_border(entity):
                    population.append(entity)
                    if is_student:
                        entity.id = teacher.id
                        teacher.students.append(entity)
                    break
                attempts += 1

    def is_entity_overlapping(self, entity, population):
        for other_entity in population:
            if entity is not other_entity:
                distance = self.get_distance(entity, other_entity)
                min_distance = self.teacher_size * 2 if entity.is_student else self.teacher_size * 2.2 + self.student_size
                if distance < min_distance:
                    return True
        return False

    def get_distance(self, entity1, entity2):
        return math.sqrt((entity1.x - entity2.x) ** 2 + (entity1.y - entity2.y) ** 2)

    def is_entity_at_border(self, entity):
        margin = self.teacher_size * 2 + self.student_size * 4.4
        return (
                entity.x < margin
                or entity.y < margin
                or entity.x > self.screenSize - margin
                or entity.y > self.screenSize - margin
        )

    def spawn_student_near_teacher(self, student, teacher):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(self.teacher_size + self.student_size * 2.2,
                                  self.teacher_size + self.student_size * 4.4)
        student.x = teacher.x + int(distance * math.cos(angle))
        student.y = teacher.y + int(distance * math.sin(angle))

    def check_teacher_burnout(self):
        # Collect the teachers who will be removed and their students
        teachers_to_remove = []
        students_to_reassign = []

        for teacher in self.teachers:
            if teacher.alive:
                # Calculate the burnout threshold for this teacher
                burnout_threshold = teacher.burnout * len(teacher.students) * teacher.age

                # Generate a random number to compare with the threshold
                random_threshold = random.uniform(0, 100)

                if burnout_threshold > random_threshold:
                    # Teacher is burned out, add to the removal list
                    teachers_to_remove.append(teacher)
                    students_to_reassign.extend(teacher.students)

        # Remove burned out teachers
        self.teachers = [teacher for teacher in self.teachers if teacher not in teachers_to_remove]

        # Reassign students to random teachers
        for student in students_to_reassign:
            if self.teachers:
                new_teacher = random.choice(self.teachers)
                new_teacher.students.append(student)
                self.spawn_student_near_teacher(student, new_teacher)

    def run(self):
        self.create_population(100, is_student=False)
        self.create_population(1000, is_student=True)
        stop = False

        while not stop:
            dt = self.clock.tick(60)
            pygame.display.update()
            self.screen.screen.fill((100, 100, 100))

            self.years_passed += 1 / dt / 10

            if round(self.years_passed) > self.year:
                self.year = round(self.years_passed)
                print(self.year)
                self.check_teacher_burnout()

            for teacher in self.teachers:
                if teacher.alive:
                    pygame.draw.circle(self.screen.screen, teacher.colour, (teacher.x, teacher.y), self.teacher_size)
                    for student in teacher.students:
                        pygame.draw.circle(self.screen.screen, student.colour, (student.x, student.y), self.student_size)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    stop = True
                    break