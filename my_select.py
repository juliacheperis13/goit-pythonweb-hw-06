from models import (
    Student,
    Teacher,
    Subject,
    Grade,
    Group,
)
from connect import session
from sqlalchemy import select, func


def select_1():
    stmt = (
        select(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(5)
    )

    result = session.execute(stmt).all()
    return [(row.name, row.average_grade) for row in result]


def select_2(subject_name):
    stmt = (
        select(Student.name, func.avg(Grade.value).label("average_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.value).desc())
        .limit(1)
    )

    result = session.execute(stmt).all()
    if result:
        return result[0].name, result[0].average_grade
    else:
        return None


def select_3(subject_name):
    stmt = select(
        Group.name.label("group_name"), func.avg(Grade.value).label("average_grade")
    ).select_from(Group)
    stmt = stmt.join(Student, Student.group_id == Group.id)
    stmt = stmt.join(Grade, Grade.student_id == Student.id)
    stmt = (
        stmt.join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .order_by(Group.name)
    )

    result = session.execute(stmt).all()
    return [(row.group_name, row.average_grade) for row in result]


def select_4():
    stmt = select(func.avg(Grade.value).label("average_grade")).select_from(Grade)
    stmt = stmt.join(Student, Student.id == Grade.student_id)

    result = session.execute(stmt).all()

    if result:
        return result[0].average_grade
    else:
        return None


def select_5(teacher_name):
    stmt = select(Subject.name).join(Teacher).filter(Teacher.name == teacher_name)
    result = session.execute(stmt).all()
    return [row.name for row in result]


def select_6(group_name):
    stmt = select(Student.name).join(Group).filter(Group.name == group_name)
    result = session.execute(stmt).all()
    return [row.name for row in result]


def select_7(group_name, subject_name):
    stmt = (
        select(Student.name, Grade.value)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
    )

    result = session.execute(stmt).all()
    return [(row.name, row.value) for row in result]


def select_8(teacher_name):
    stmt = (
        select(func.avg(Grade.value).label("average_grade"))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
    )
    result = session.execute(stmt).all()
    return result[0][0] if result else None


def select_9(student_name):
    stmt = (
        select(Subject.name)
        .distinct()
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
    )
    result = session.execute(stmt).all()
    return [row.name for row in result]


def select_10(student_name, teacher_name):
    stmt = (
        select(Subject.name)
        .distinct()
        .join(Teacher)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
    )
    result = session.execute(stmt).all()
    return [row.name for row in result]


# Run the queri
if __name__ == "__main__":
    print("Top 5 students by average grade:", select_1())
    print("Top student in Math:", select_2("Math"))
    print("Average grade in Math by group:", select_3("Math"))
    print("Overall average grade:", select_4())
    print("Courses taught by Michael Mcdonald:", select_5("Michael Mcdonald"))
    print("Students in Group 1:", select_6("Group 1"))
    print("Grades in Group 1 for Math:", select_7("Group 1", "Math"))
    print("Average grade given by Michael Mcdonald", select_8("Michael Mcdonald"))
    print("Courses attended by Kathy Arnold:", select_9("Kathy Arnold"))
    print(
        "Courses attended by Kathy Arnold taught by Michael Mcdonald:",
        select_10("Kathy Arnold", "Michael Mcdonald"),
    )
