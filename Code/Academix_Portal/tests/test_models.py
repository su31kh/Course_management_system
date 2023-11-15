from django.test import TestCase
from django.contrib.auth.models import User

from Academix_Portal.models import student_profile,faculty_profile,Course
from django.db.utils import IntegrityError

## Notes for people involved in testing ##

"""
1. class name should start with 'Test'.
2. testing function name should start with 'test_'
3. instance creation name should always be SetUp
4. if you are creating any files under tests folder, make sure the filename is starting with test as django looks for test under test folder

5. for running test use python manage.py test Academix_Portal
6. Save the console output in textfile. few sample test case are provided 3 of them are true and one is wrong
   in line 82. 1 != 2 since in line 80, i have added only 1 course i.e Computer Science 101 to faculty aakash.
   (you can read console output sample in model_test.txt)

"""

from django.test import TestCase
from django.contrib.auth.models import User
from Academix_Portal.models import student_profile, faculty_profile, Course

class TestModels(TestCase):
    def setUp(self):
        self.user_student = User.objects.create_user(username='shrikar', password='shrikar123')
        self.user_faculty = User.objects.create_user(username='aakash', password='aakash123')

        self.faculty = faculty_profile.objects.create(
            user=self.user_faculty,
            first_name='aakash',
            middle_name='xyz',
            last_name='patel'
        )

        self.student = student_profile.objects.create(
            user=self.user_student,
            first_name='shrikar',
            middle_name='shaileshbhai',
            last_name='padaliya',
            batch=2022,
            branch='ICT',
            program='B.Tech'
        )

        self.course = Course.objects.create(
            name='Computer Science 101',
            course_code='CS101',
            description='Introduction to Computer Science',
            faculty=self.faculty
        )

    def test_duplicate_usernames(self):
        # Test for uniqueness of usernames
        user_duplicate = User(username='shrikar', password='testpassword')
        with self.assertRaises(Exception):
            user_duplicate.save()

    def test_student_enroll_in_course(self):
        # Test if a student can enroll in a course
        self.course.studentlist.add(self.student)
        self.assertEqual(self.course.studentlist.count(), 1)

    def test_course_with_no_faculty(self):
        # Test creating a course without a faculty
        
        with self.assertRaises(IntegrityError):
            course_no_faculty = Course.objects.create(
            name='No Faculty Course',
            course_code='NF101',
            description='Course without faculty'
        )

    def test_course_without_students(self):
        # Test creating a course without students
        course_empty = Course.objects.create(
            name='Empty Course',
            course_code='EC101',
            description='Course with no students',
            faculty=self.faculty
        )
        self.assertEqual(course_empty.studentlist.count(), 0)

    def test_student_courses_relationship(self):
        # Testing relationship between student and courses
        self.student.student_courses.add(self.course)
        self.assertEqual(self.student.student_courses.count(), 1)
        self.assertEqual(self.student.student_courses.first().name, 'Computer Science 101')

    def test_faculty_courses_relationship(self):
        # Testing relationship between faculty and courses
        self.faculty.faculty_courses.add(self.course)
        self.assertEqual(self.faculty.faculty_courses.count(), 1)
        self.assertEqual(self.faculty.faculty_courses.first().name, 'Computer Science 101')

    def test_course_students_and_faculty(self):
        # Testing that a course has both students and a faculty
        self.course.studentlist.add(self.student)
        self.assertEqual(self.course.studentlist.count(), 1)
        self.assertEqual(self.course.faculty, self.faculty)

    def test_student_str_method(self):
        
        self.assertEqual(str(self.student), 'shrikar')

    def test_faculty_str_method(self):
        
        self.assertEqual(str(self.faculty), 'aakash')

    def test_course_str_method(self):
        
        self.assertEqual(str(self.course), 'Computer Science 101')
