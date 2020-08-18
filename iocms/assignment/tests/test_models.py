from django.test import TestCase
from assignment.models import Assignment , Teacher, Student, AssignmentByStudent


class TestModels(TestCase):

    def setUp(self):

        self.teacher1 = Teacher.objects.create(
            full_name = "John Doe",
            email = "john@john.com"
        )

        self.assignment1 = Assignment.objects.create(
            teacher = self.teacher1,
            title = 'Python Function',
            points = 5, 
            deadline = '2020-11-20T15:58:44.767594-06:00'
        )
        self.student1 = Student.objects.create(
            full_name = "Ram Khadka",
            email = "ram@gmal.com"
        )

    #For Teacher Model
    def test_teacher_model(self):
        self.assertEquals(self.teacher1.full_name, 'John Doe')

    #For Assignment model
    def test_assignment_model(self):
        
        self.assertEquals(Assignment.objects.first().title, 'Python Function')
        

    #For assignment which is posted by teacher
    def test_assignment_post_by_teacher(self):
        self.assertEquals(self.assignment1.title, 'Python Function')

    def test_assignment_submit_by_student(self):
        assignment_answer = AssignmentByStudent.objects.create(
            student = self.student1,
            assignment_details = self.assignment1,
            assignment_link = "https://www.fb.com",
            
        )
        self.assertEquals(assignment_answer.assignment_link, "https://www.fb.com")

    