 
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
    connect("fast-api-database", host="mongo", port=27017)


@app.on_event("shutdown")
def shutdown_db_client():
    # Set the correct parameters to disconnect from the database
    disconnect("fast-api-database")


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

def filter_by_student_name(courses, student_name):
    if student_name == '':
        return courses
    
    print(f"filtering by student name: {student_name}")
    
    students = [student_to_json(student) for student in Student.objects(name=student_name)]

    print(f"found students: {students}")

    return [course for course in courses if len([student for student in students if student["id"] in course["students"]]) > 0]

def filter_by_tag(courses, tag):
    if tag == '':
        return courses
    
    return [course for course in courses if tag in course["tags"]]

# Schema

class Student(Document):
    # Implement the Student schema according to the instructions
    # name	String	required:true
    # student_number	Number	–
    name = StringField(required=True)
    student_number = IntField()

class Course(Document):
    # Implement the Course schema according to the instructions
    # name	String	required:true
    # description	String	–
    # tags	List of Strings	–
    # students	List of Student References	–
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField("Student", reverse_delete_rule=4))
    

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
@app.post("/students", status_code=201)
def create_student(student: StudentData):
    new_student = Student(**student.dict()).save()
    return {"message": "Student successfully created", "id": f"${new_student.id}"}

@app.get('/students/{student_id}')
def get_students(student_id: str):
    student = Student.objects.get(id=student_id)
    return student_to_json(student)

@app.put("/students/{student_id}")
def update_movie(student_id: str, student: StudentData):
    Student.objects.get(id=student_id).update(**student.dict())
    return {"message": "Student succesfully updated"}

@app.delete("/students/{student_id}")
def delete_movie(student_id: str):
    Student.objects(id=student_id).delete()
    return {"message" : "Student successfully deleted"}


# Course routes
# Complete the Course routes similarly as per the instructions provided in A+
@app.post("/courses", status_code=201)
def create_course(course: CourseData):
    new_course = Course(**course.dict()).save()
    return {"message": "Course successfully created", "id": f"${new_course.id}"}

@app.get('/courses')
def get_courses(tag: str = "", studentName: str = ""):
    coursesObjects = Course.objects
    courses = []
    for courseObject in coursesObjects:
        courses += [ course_to_json(courseObject) ]

    courses = filter_by_student_name(courses, studentName)
    courses = filter_by_tag(courses, tag)
    return courses

@app.get('/courses/{course_id}')
def get_courses(course_id: str):
    course = Course.objects.get(id=course_id)
    return course_to_json(course)

@app.put("/courses/{course_id}")
def update_movie(course_id: str, course: CourseData):
    Course.objects.get(id=course_id).update(**course.dict())
    return {"message": "Course succesfully updated"}

@app.delete("/courses/{course_id}")
def delete_movie(course_id: str):
    Course.objects(id=course_id).delete()
    return {"message" : "Course successfully deleted"}
