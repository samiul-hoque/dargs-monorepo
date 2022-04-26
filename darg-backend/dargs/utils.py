import pandas as pd
from dargs import models
from MySQLdb import _mysql
from django.core.management import call_command
from tqdm import tqdm


def reset_db():
    db = _mysql.connect(
        host="127.0.0.1",
        user="root",
        password="example",
    )
    try:
        db.query("DROP DATABASE dargs;")
    except:
        pass
    try:
        db.query("CREATE DATABASE dargs;")
    except:
        pass
    db.close()


def preprocess(df, filename):
    _, semester_name, semester_year = (
        "".join(filename.split("/")[-1]).replace(".csv", "").split()
    )
    df = df.reset_index(drop=True)
    df["SEMESTER_NAME"] = semester_name.lower()
    df["SEMESTER_YEAR"] = semester_year
    return df


def insert_to_db(df):
    for rec in tqdm(df.to_dict("records")):
        department_code = rec["COFFER_COURSE_ID"][:3]
        faculty_id, faculty_name, *_ = rec["FACULTY_FULL_NAME"].split("-")
        program = models.Program.objects.create()

        try:
            faculty = models.Faculty.objects.get(Faculty_ID=faculty_id)
        except:
            faculty = models.Faculty.objects.create(
                Faculty_ID=faculty_id, Faculty_Name=faculty_name
            )

        try:
            department = models.Department.objects.get(Department_Code=department_code)
        except:
            department = models.Department.objects.create(
                Department_Code=department_code
            )

        school, _ = models.School.objects.get_or_create(School_name=rec["SCHOOL_TITLE"])
        try:
            course = models.Course.objects.get(Course_ID=rec["COFFER_COURSE_ID"])
        except:
            course = None
        if course is None:
            course = models.Course.objects.create(
                School=school,
                Course_ID=rec["COFFER_COURSE_ID"],
                Course_name=rec["COURSE_NAME"],
                Credit_hours=rec["CREDIT_HOUR"],
                Co_Offered=rec["COFFERED_WITH"],
            )

        try:
            semester = models.Semester.objects.get(
                Year=rec["SEMESTER_YEAR"],
                Semester_name=rec["SEMESTER_NAME"].lower(),
            )
        except:
            semester = None

        if semester is None:
            semester = models.Semester.objects.create(
                Year=rec["SEMESTER_YEAR"],
                Semester_name=rec["SEMESTER_NAME"].lower(),
            )

        room, _ = models.Room.objects.get_or_create(
            Room_ID=rec["ROOM_ID"], Room_capacity=rec["ROOM_CAPACITY"]
        )
        _class = models.Class.objects.create(
            Section_No=rec["SECTION"],
            Room_ID=room,
            Course_ID=course,
            Capacity=rec["CAPACITY"],
            Enrolled=rec["ENROLLED"],
            Start_time=rec["STRAT_TIME"],
            End_time=rec["END_TIME"],
            Course_Day=rec["ST_MW"],
            Faculty_ID=faculty,
            Semester_ID=semester,
            Department_ID=department,
            Program_ID=program,
        )
