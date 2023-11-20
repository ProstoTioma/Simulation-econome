import math
import random

import pygame

from entity import Entity
from screen import Screen

random.seed(42)


class Simulation:
    def __init__(self):
        self.screenSize = 900
        self.colours = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
        self.clock = pygame.time.Clock()
        self.students = []
        self.teachers = []
        self.teacher_conversion_rate = 4
        self.teacher_completion_rate = 60
        self.years_passed = 0
        self.year = 0
        self.teacher_size = 10
        self.student_size = 2
        self.student_spawn_radius = 5
        self.screen = Screen(self.screenSize, self.screenSize)

        self.data = "Year Students Teachers \n"

        self.file_path = "data.txt"

        self.spawn_new_students = 300
        self.entity_id_counter = 1  # New global ID counter

    def create_entity(self, is_student, is_new=False):
        age = random.randint(25, 35) if not is_student else random.randint(0, 15)
        if is_new:
            age = 0 if random.randint(0, 10) < 7 else random.randint(0, 15)
        color = (200, 200, 200) if not is_student else random.choice(self.colours)
        x, y = random.randint(0, self.screenSize), random.randint(0, self.screenSize)
        entity = Entity(self.entity_id_counter, age, color, x, y, is_student=is_student)
        self.entity_id_counter += 1  # Increment the global ID counter
        return entity

    def create_population(self, n, is_student=True, is_new=False):
        population = self.students if is_student else self.teachers
        max_attempts = 10  # Maximum attempts to create non-overlapping entity
        for i in range(n):
            attempts = 0
            while attempts < max_attempts:
                entity = self.create_entity(is_student, is_new)
                if is_student:
                    if self.teachers:
                        teacher = random.choice(self.teachers)
                        self.spawn_student_near_teacher(entity, teacher)
                if not self.is_entity_overlapping(entity, population) and not self.is_entity_at_border(entity):
                    population.append(entity)
                    if is_student:
                        if self.teachers:
                            entity.id = teacher.id
                            teacher.students.append(entity)
                    break
                attempts += 1
            if attempts == max_attempts:
                entity = self.create_entity(is_student, is_new)
                if is_student and len(self.teachers) > 0:
                    teacher = random.choice(self.teachers)
                    self.spawn_student_near_teacher(entity, teacher)
                    entity.id = teacher.id
                    teacher.students.append(entity)
                population.append(entity)

    def is_entity_overlapping(self, entity, population):
        for other_entity in population:
            if entity is not other_entity:
                distance = self.get_distance(entity, other_entity)
                min_distance = self.teacher_size * 2 if entity.is_student else self.teacher_size * 4.4 + self.student_size
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

                if burnout_threshold > random_threshold or teacher.age > 65:
                    # Teacher is burned out, add to the removal list
                    teachers_to_remove.append(teacher)
                    students_to_reassign.extend(teacher.students)

        # Remove burned out teachers
        self.teachers = [teacher for teacher in self.teachers if teacher not in teachers_to_remove]

        # Reassign students to random teachers
        self.reassign_students(students_to_reassign)

    def reassign_students(self, students_to_reassign):
        for student in students_to_reassign:
            if len(self.teachers) > 0:
                new_teacher = random.choice(self.teachers)
                new_teacher.students.append(student)
                student.id = new_teacher.id
                self.spawn_student_near_teacher(student, new_teacher)

    def run(self):
        self.create_population(100, is_student=False)
        self.create_population(2000, is_student=True)

        while True:  # Simplified loop condition
            dt = self.clock.tick(60)
            pygame.display.update()
            self.screen.screen.fill((100, 100, 100))

            self.years_passed += 1 / dt

            if round(self.years_passed) > self.year:
                new_teachers = self.students_to_teachers(self.students)
                for _ in new_teachers:
                    self.create_population(1, False)

                self.year = round(self.years_passed)
                print("Year: ", self.year)
                self.check_teacher_burnout()
                print(f"Students: {len(self.students)}, Teachers: {len(self.teachers)}, Students/Teachers: {len(self.students) // (len(self.teachers) + 1)}")
                self.create_population(self.spawn_new_students, is_student=True, is_new=True)
                self.data += f"{self.year} {len(self.students)} {len(self.teachers)}\n"
                self.teachers = [teacher for teacher in self.teachers if teacher.alive]
                for teacher in self.teachers:
                    teacher.students = []
                self.reassign_students(self.students)

            for teacher in self.teachers:
                if teacher.alive:
                    teacher.live(dt)
                    pygame.draw.circle(self.screen.screen, teacher.colour, (teacher.x, teacher.y), self.teacher_size)
                    for student in teacher.students:
                        student.live(dt)
                        pygame.draw.circle(self.screen.screen, student.colour, (student.x, student.y),
                                           self.student_size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    with open(self.file_path, 'w') as file:
                        # Write the data to the file
                        file.write(self.data)

                    break

    def students_to_teachers(self, students):
        new_teachers = []
        students_to_remove = []
        for student in students:
            if student.age > 12 and not student.is_studying:
                if random.uniform(0, 100) < self.teacher_conversion_rate:
                    student.is_studying = True
                else:
                    students_to_remove.append(student)
            elif student.is_studying and student.age > 16:
                if random.uniform(0, 100) < self.teacher_completion_rate:
                    new_teachers.append(student)
                    students_to_remove.append(student)

        for st in students_to_remove:
            students.remove(st)
            for teacher in self.teachers:
                if st in teacher.students:
                    teacher.students.remove(st)
                    break

        return new_teachers
