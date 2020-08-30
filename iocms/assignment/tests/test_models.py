from django.test import TestCase
from users.models import User, Teacher, Student
from classroom.models import Classroom
from assignment.models import Assignment , AssignmentByStudent



class TestModels(TestCase):

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
        self.class1 = Classroom.objects.create(
            class_name = "Django",
            created_by = self.teacher,

        )

        self.assignment1 = Assignment.objects.create(
            class_name = self.class1,
            teacher = self.teacher,
            title = 'Python Function',
            points = 5, 
            deadline = '2020-11-20T15:58:44.767594-06:00'
        )
        

   
    #For Assignment model
    def test_assignment_model(self):
        
        self.assertEquals(Assignment.objects.first().title, 'Python Function')
        

    #For assignment which is posted by teacher
    def test_assignment_post_by_teacher(self):
        self.assertEquals(self.assignment1.title, 'Python Function')


    def test_assignment_submit_by_student(self):
        assignment_answer = AssignmentByStudent.objects.create(
            student = self.student ,
            assignment_details = self.assignment1,
            assignment_link = "https://www.fb.com",
            
        )
        self.assertEquals(assignment_answer.assignment_link, "https://www.fb.com")

    