from django.test import TestCase
from users.models import Student, Teacher, User


class StudentTestCase(TestCase):

    def setUp(self):

        self.student_user = User.objects.create(
            username="johnbro",
            first_name="john",
            last_name="doe",
            email="johndoe@example.com"
        )

        self.teacher_user = User.objects.create(
            username="johnbro_t",
            first_name="johntea",
            last_name="doe",
            email="johndoe_tea@example.com"
        )

        self.student = Student.objects.create(
            user=User.objects.get(id=1)
        )

        self.teacher = Teacher.objects.create(
            user=User.objects.get(id=2)
        )

    def test_first_name(self):
        student1 = self.student.user.first_name
        teacher1 = self.teacher.user.first_name
        self.assertEquals(student1, 'john')
        self.assertEquals(teacher1, 'johntea')

    def test_email(self):
        student1 = self.student.user.email
        teacher1 = self.teacher.user.email
        self.assertEquals(student1, 'johndoe@example.com')
        self.assertEquals(teacher1, 'johndoe_tea@example.com')

    def test_user_type(self):
        student1 = self.student.user.is_teacher
        teacher1 = self.teacher.user.is_student
        self.assertFalse(student1)
        self.assertFalse(teacher1)
