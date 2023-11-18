from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Academix_Portal.models import student_profile,faculty_profile,Course,Assignment,Submission,query,Announcements,Material,feedback
from datetime import datetime

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
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

        self.assignment = Assignment.objects.create(
            name='Assignment 1',
            description='First assignment',
            duedate=datetime(2023, 12, 1, 0, 0, 0),
            max_grade=100,
            attachment='aakash_assignment1',
            assignment_course=self.course
        )

        
        self.my_course_url = reverse('mycourse')
        self.view_assignments_url = reverse('view_assignments', args=['CS101'])
        self.profile_url = reverse('students_profile')
        self.view_announcements_url = reverse('announcements', args=['CS101'])
        self.view_materials_url = reverse('materials', args=['CS101'])
        self.view_query_url = reverse('view_query', args=['CS101'])
        self.view_feedback_url = reverse('feedback', args=['CS101'])
        self.view_student_list_url = reverse('student_list', args=['CS101'])
        self.add_assignment_url = reverse('add_assignment', args=['CS101'])
        self.add_announcement_url = reverse('addannouncement', args=['CS101'])
        self.add_submission_url = reverse('add_submission', args=['CS101', 'Assignment 1'])

    #testing view enrolled courses page
    def test_my_course_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.my_course_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_course_student.html')
        self.assertTemplateUsed(response, 'base.html')

    #tests for view assignment page faculty side    
    def test_view_assignments_faculty_GET(self):
        login = self.client.login(username='aakash', password='aakash123')
        response = self.client.get(self.view_assignments_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_assignments_faculty.html')

    #tests for view assignment page student side
    def test_view_assignments_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_assignments_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_assignments.html')
        self.assertTemplateUsed(response, 'navbar.html')

    #tests for view profile page
    def test_view_profile_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_profile.html')
    
    #tests for view announcements page
    def test_view_announcements_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_announcements_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'announcements.html')

    #tests for view materials page
    def test_view_materials_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_materials_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'materials.html')

    #tests for view query page
    def test_view_query_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_query_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_query.html')

    #tests for view feedback page student side
    def test_view_feedback_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_feedback_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback_student.html')

    #tests for view feedback page faculty side
    def test_view_feedback_faculty_GET(self):
        login = self.client.login(username='aakash', password='aakash123')
        response = self.client.get(self.view_feedback_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback_faculty.html')

    #tests for view enrolled student list
    def test_view_student_list_GET(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        response = self.client.get(self.view_student_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_list.html')

    #tests for adding assignment
    def test_add_assignment_POST(self):
        login = self.client.login(username='aakash', password='aakash123')
        data = {
            'name' : 'Assignment 2',
            'max_grade': '100',
            'description' : 'Second assignment',
            'duedate' : datetime(2023, 12, 1, 0, 0, 0),
            'attachment' : 'https://github.com',
            'assignment_course' : self.course}
        
        response = self.client.post(self.add_assignment_url, data)
        self.assertEquals(response.status_code, 302)
        assignment = Assignment.objects.get(name = "Assignment 2")
        self.assertEqual(assignment.description, 'Second assignment')

    #tests for adding announcement
    def test_add_announcement_POST(self):
        login = self.client.login(username='aakash', password='aakash123')
        data = {
            'user' : self.user_faculty,
            'course' : self.course,
            'title': 'Lecture file',
            'description' : 'PFA materials',
            'timestamp' :  datetime(2023, 12, 1, 0, 0, 0)}
    

        response = self.client.post(self.add_announcement_url, data)
        self.assertEquals(response.status_code, 302)

    #tests for adding submission
    def test_add_submission_POST(self):
        login = self.client.login(username='shrikar', password='shrikar123')
        data = {
            'student' : self.student,
            'work' : 'https://github.com',
            'title': 'Lecture file',
            'assignment' : self.assignment,
            'timestamp' :  datetime(2023, 12, 1, 0, 0, 0)}
    

        response = self.client.post(self.add_submission_url, data)
        self.assertEquals(response.status_code, 302)
