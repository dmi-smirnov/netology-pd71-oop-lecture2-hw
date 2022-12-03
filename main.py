class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __str__(self):
        return (f'Имя: {self.name}\n' +
            f'Фамилия: {self.surname}')

class Graded:
    def __init__(self):
        self.grades = {}

    def __lt__(self, graded):
        if isinstance(graded, Graded) and type(self) == type(graded):
            return self.get_average_grade() < graded.get_average_grade()
        else:
            return 'Error.'

    def get_average_grade(self):
        average_grades = []
        for course_grades in self.grades.values():
            average_grades.append(sum(course_grades) / len(course_grades))
        return round(sum(average_grades) / len(average_grades), 1)

class Student(Person, Graded):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        Graded.__init__(self)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def __str__(self):
        return (super().__str__() +
            '\n' +
            'Средняя оценка за домашние задания: ' +
            str(self.get_average_grade()) +
            '\n' +
            'Курсы в процессе изучения: ' +
            ', '.join(c for c in self.courses_in_progress) +
            '\n' +
            'Завершённые курсы: ' +
            ', '.join(c for c in self.finished_courses))

    def rate_lecturer(self, lecturer, course, grade):
        if (course in self.courses_in_progress
        and isinstance(lecturer, Lecturer)
        and course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

class Mentor(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

class Lecturer(Mentor, Graded):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        Graded.__init__(self)
        
    def __str__(self):
        return (super().__str__() + '\n' +
              f'Средняя оценка за лекции: {self.get_average_grade()}')

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and
            course in self.courses_attached and
            course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

def get_average_grade(graded_list, course_name):
    grades_sum = 0
    grades_amount = 0
    for graded in graded_list:
        if not isinstance(graded, Graded):
            print('Error: one element of graded_list is not Graded')
            return
        if not course_name in graded.grades.keys():
            print(f'Error: dict grades of one element of graded_list does not contain a key {course_name}')
            return
        grades_sum += sum(graded.grades[course_name])
        grades_amount += len(graded.grades[course_name])
    return round(grades_sum / grades_amount, 1)

student1 = Student(
    'student1_name',
    'student1_surname',
    'student1_gender')
student1.courses_in_progress.append('Python')
student1.courses_in_progress.append('Git')
student1.finished_courses.append('Введение в программирование')

student2 = Student(
    'student2_name',
    'student2_surname',
    'student2_gender')
student2.courses_in_progress.append('Python')
student2.courses_in_progress.append('Git')
student2.finished_courses.append('Введение в программирование')

lecturer1 = Lecturer('lecturer1_name', 'lecturer1_surname')
lecturer1.courses_attached.append('Python')
lecturer1.courses_attached.append('Введение в программирование')

lecturer2 = Lecturer('lecturer2_name', 'lecturer2_surname')
lecturer2.courses_attached.append('Python')
lecturer2.courses_attached.append('Git')

reviewer1 = Reviewer('reviewer1_name', 'reviewer1_surname')
reviewer1.courses_attached.append('Python')

reviewer2 = Reviewer('reviewer2_name', 'reviewer2_surname')
reviewer2.courses_attached.append('Git')

reviewer1.rate_hw(student1, 'Python', 8)
reviewer1.rate_hw(student1, 'Python', 9)

reviewer1.rate_hw(student2, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 9)

reviewer2.rate_hw(student1, 'Git', 7)
reviewer2.rate_hw(student1, 'Git', 8)

reviewer2.rate_hw(student2, 'Git', 8)
reviewer2.rate_hw(student1, 'Git', 10)

student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer2, 'Python', 7)
student1.rate_lecturer(lecturer2, 'Git', 5)

student2.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Git', 6)

print(student1, student2,
    lecturer1, lecturer2,
    reviewer1, reviewer2,
    sep='\n\n', end='\n\n')

print('student1 average grade:', student1.get_average_grade())
print('student2 average grade:', student2.get_average_grade())
print('student1 < student2:', student1 < student2, end='\n\n')

print('lecturer1 average grade:', lecturer1.get_average_grade())
print('lecturer2 average grade:', lecturer2.get_average_grade())
print('lecturer1 < lecturer2:', lecturer1 < lecturer2, end='\n\n')

print('Средняя оценка за ДЗ у student1 и student2 по курсу Python:',
    get_average_grade([student1, student2], 'Python'), end='\n\n')

print('Средняя оценка за ДЗ у student1 и student2 по курсу Git:',
    get_average_grade([student1, student2], 'Git'), end='\n\n')

print('Средняя оценка за лекции у lecturer1 и lecturer2 по курсу Python:',
    get_average_grade([lecturer1, lecturer2], 'Python'), end='\n\n')