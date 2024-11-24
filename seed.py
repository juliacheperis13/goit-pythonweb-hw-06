from faker import Faker
from models import Base, Group, Student, Teacher, Subject, Grade
from random import randint, choice
from datetime import date, timedelta
from connect import session, engine

unique_subject_names = [
    "Chemistry",
    "Math",
    "Biology",
    "English",
    "French",
    "Philosophy",
    "Economics",
]
fake = Faker()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=randint(0, delta.days))


# Generate and seed data
def seed_database():
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)

    teachers = [Teacher(name=fake.name()) for _ in range(4)]
    session.add_all(teachers)

    subjects = [
        Subject(name=subject_name, teacher=choice(teachers))
        for subject_name in unique_subject_names
    ]
    session.add_all(subjects)
    students = [Student(name=fake.name(), group=choice(groups)) for _ in range(40)]
    session.add_all(students)

    start_date = date(2023, 1, 1)
    end_date = date(2024, 1, 1)
    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(randint(5, 20)):  # Random number of grades
                grade = Grade(
                    value=randint(1, 12),  # Grades between 1 and 12
                    date=random_date(start_date, end_date),
                    student=student,
                    subject=subject,
                )
                grades.append(grade)

    session.add_all(grades)

    # Commit changes
    session.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
