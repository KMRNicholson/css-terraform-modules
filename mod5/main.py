 
from fastapi import FastAPI
from mongoengine import (
    connect,
    disconnect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    IntField
)
import json
from pydantic import BaseModel

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    # Set the correct parameters to connect to the database
    connect("", host="", port=)


@app.on_event("shutdown")
def shutdown_db_client():
    # Set the correct parameters to disconnect from the database
    disconnect("")


# Helper functions to convert MongeEngine documents to json

def course_to_json(course):
    course = json.loads(course.to_json())
    course["students"] = list(map(lambda dbref: str(dbref["$oid"]), course["students"]))
    course["id"] = str(course["_id"]["$oid"])
    course.pop("_id")
    return course


def student_to_json(student):
    student = json.loads(student.to_json())
    student["id"] = str(student["_id"]["$oid"])
    student.pop("_id")
    return student

# Schema

class Student(Document):
    # Implement the Student schema according to the instructions


class Course(Document):
    # Implement the Course schema according to the instructions
    

# Input Validators

class CourseData(BaseModel):
    name: str
    description: str | None
    tags: list[str] | None
    students: list[str] | None


class StudentData(BaseModel):
    name: str
    student_number: int | None


# Student routes
# Complete the Student routes similarly as per the instructions provided in A+


# Course routes
# Complete the Course routes similarly as per the instructions provided in A+

