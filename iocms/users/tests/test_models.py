from django.test import TestCase
from .models import Student, Teacher


class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(username="student1",
                               first_name="gaurav",
                               last_name="jaiswal",
                               email='email1@gmail.com'
                               )

    def test_first_name_label(self):
        author = Student.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')



class TeacherTestCase(TestCase):
    def setUp(self):
        Teacher.objects.create(
                               first_name="gaurav",
                               last_name="jaiswal",
                               email='email1@gmail.com'
                               )
