from configparser import SectionProxy
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import CharField
from pyparsing import Char

# Create your models here.
class School(models.Model):
    School_ID = models.AutoField(primary_key=True)
    School_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.School_ID} | {self.School_name}"


class Course(models.Model):
    Course_ID = models.CharField(max_length=10, primary_key=True, unique=True)
    School = models.ForeignKey(School, to_field="School_ID", on_delete=models.CASCADE)
    Course_name = models.CharField(max_length=255, null=False, blank=False)
    Credit_hours = models.IntegerField(null=False, blank=False)
    Co_Offered = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.Course_ID} | {self.Course_name}"


class Semester(models.Model):
    Semester_ID = models.AutoField(primary_key=True)
    Year = models.IntegerField(null=False, blank=False)
    Semester_name = models.CharField(
        max_length=20,
        choices=[("spring", "spring"), ("summer", "summer"), ("autumn", "autumn")],
        null=False,
        blank=False,
    )

    def __str__(self) -> str:
        return f"{self.Semester_ID} | {self.Year} | {self.Semester_name}"


class Room(models.Model):
    Room_ID = models.CharField(max_length=10, primary_key=True)
    Room_capacity = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.Room_ID} | {self.Room_capacity}"


class Department(models.Model):
    Department_ID = models.AutoField(primary_key=True)
    Department_Code = models.CharField(max_length=10, null=True, blank=True)


class Program(models.Model):
    Program_ID = models.AutoField(primary_key=True)
    Program_code = models.CharField(max_length=10, null=True, blank=True)


class Faculty(models.Model):
    Faculty_ID = models.CharField(max_length=20, primary_key=True)
    Faculty_Name = models.CharField(
        max_length=255, null=False, blank=False, unique=True
    )


class Class(models.Model):
    Class_ID = models.AutoField(primary_key=True)
    Section_No = models.CharField(max_length=10, null=False, blank=False)
    Room_ID = models.ForeignKey(
        Room, to_field="Room_ID", blank=False, on_delete=models.CASCADE
    )
    Course_ID = models.ForeignKey(
        Course, to_field="Course_ID", on_delete=models.CASCADE
    )
    Capacity = models.IntegerField(null=False, blank=False)
    Enrolled = models.IntegerField(null=False, blank=False)
    Faculty_ID = models.ForeignKey(
        Faculty, to_field="Faculty_ID", on_delete=models.CASCADE
    )
    Start_time = models.CharField(max_length=50, null=False, blank=False)
    End_time = models.CharField(max_length=50, null=False, blank=False)
    Course_Day = models.CharField(
        max_length=50,
        choices=[("ST", "ST"), ("MW", "MW"), ("R", "R"), ("A", "A")],
        null=False,
        blank=False,
    )
    Program_ID = models.ForeignKey(
        Program, to_field="Program_ID", on_delete=models.CASCADE
    )
    Department_ID = models.ForeignKey(
        Department, to_field="Department_ID", on_delete=models.CASCADE
    )
    Semester_ID = models.ForeignKey(
        Semester, to_field="Semester_ID", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.Section_No} | {self.Course_ID}"
