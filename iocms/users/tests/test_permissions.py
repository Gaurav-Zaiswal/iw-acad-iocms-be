from rest_framework.test import APITestCase

from users.permissions import IsStudentUser, IsTeacherUser


class AccountsTest(APITestCase):

    def test_user_permission(self):
        self.assertTrue(IsStudentUser)
        self.assertTrue(IsTeacherUser)
