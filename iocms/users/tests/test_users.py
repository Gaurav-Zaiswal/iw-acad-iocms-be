from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import Student, Teacher, User


class AccountsTest(APITestCase):

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

        self.student1 = Student.objects.create(
            user=User.objects.get(id=1)
        )

        self.teacher1 = Student.objects.create(
            user=User.objects.get(id=2)
        )

    def test_create_student(self):

        """
        Ensure we can create a new user.
        """
        student_data = {
            'username': 'student_one',
            'first_name': 'ram',
            'last_name': "bahadur",
            'email': 'one@email.com',
            'password': 'somepassword'
        }

        student_login_data = {
            'username': 'one@email.com',
            'password': 'somepassword'
        }

        response = self.client.post("/users/api/student-register/", student_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], student_data['username'])
        self.assertEqual(response.data['email'], student_data['email'])
        self.assertFalse('password' in response.data)

        # check whether or not token is generated
        response = self.client.post("/users/api/login/", student_login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)

    def test_create_teacher(self):

        """
        Ensure we can create a new user
        """
        teacher_data = {
            'username': 'teacher_one',
            'first_name': 'Hari',
            'last_name': "bahadur",
            'email': 'two@email.com',
            'password': 'somepassword123'
        }

        teacher_login_data = {
            'username': 'two@email.com',
            'password': 'somepassword123'
        }

        response = self.client.post("/users/api/teacher-register/", teacher_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(response.data['username'], teacher_data['username'])
        self.assertEqual(response.data['email'], teacher_data['email'])
        self.assertFalse('password' in response.data)

        # check whether or not token is generated
        response = self.client.post("/users/api/login/", teacher_login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
