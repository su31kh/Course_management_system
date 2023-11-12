from django.test import TestCase
from django.contrib.auth.models import User

from Academix_Portal.models import student_profile,faculty_profile,Course


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

        self.course2 = Course.objects.create(
            name='Mathematics 101',
            course_code='MATH101',
            description='Introduction to Mathematics',
            faculty=self.faculty
        )


    def test_student_profile_str(self):
        
        self.assertEqual(str(self.student), 'shrikar')

    def test_faculty_profile_str(self):
            
        self.assertEqual(str(self.faculty), 'aakash')

    def test_course_str(self):
           
        self.assertEqual(str(self.course), 'Computer Science 101')