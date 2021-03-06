import pandas as pd

import django
import os
import pandas as pd
from tqdm import tqdm
from MySQLdb import _mysql
from django.core.management import call_command

os.environ["DJANGO_SETTINGS_MODULE"] = "db_project.settings"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()

from dargs import models

from glob import glob

tally_filepaths = glob("./assets/tally*.csv")


def preprocess(df, filename):
    _, semester_name, semester_year = (
        "".join(filename.split("/")[-1]).replace(".csv", "").split()
    )
    df.columns = df.iloc[2].values.tolist()
    df = df[3:-2]
    df = df.reset_index(drop=True)
    df["SEMESTER_NAME"] = semester_name.lower()
    df["SEMESTER_YEAR"] = semester_year
    return df


def reset_db():
    db = _mysql.connect(host="localhost", user="root", password="example")
    try:
        db.query("DROP DATABASE dargs;")
    except:
        pass
    try:
        db.query("CREATE DATABASE dargs;")
    except:
        pass
    db.close()


def seed_db(dataframe):
    for index, rec in tqdm(enumerate(dataframe.to_dict(orient="records")), total=dataframe.shape[0]):
        #print(rec)
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

        models.AggregratedMaterializedView.objects.create(**rec)
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
                Co_Offered=rec["COFFERED_WITH"]
            )

        try:
            semester = models.Semester.objects.get(
                Year=rec["SEMESTER_YEAR"], Semester_name=rec["SEMESTER_NAME"].lower()
            )
        except:
            semester = None

        if semester is None:
            semester = models.Semester.objects.create(
                Year=rec["SEMESTER_YEAR"], Semester_name=rec["SEMESTER_NAME"].lower()
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


df = pd.concat(
    [preprocess(pd.read_csv(filepath), filepath) for filepath in tally_filepaths]
)


reset_db()
call_command("makemigrations", "dargs")
call_command("migrate", "dargs")
call_command("migrate")
seed_db(df)
