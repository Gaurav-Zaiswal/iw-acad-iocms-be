from django.test import SimpleTestCase
from django.urls import resolve, reverse
from assignment.views import AssignmentView, AssignmentDetailView, AssignmentSubmitView

class TestUrl(SimpleTestCase):

    #test for url:  assignment/list
    def test_assignment_list_url(self):
        url = reverse('assignment:list')
        self.assertEquals(resolve(url).func.view_class, AssignmentView) 

    #test for url:  assignment/list<int:pk>
    def test_assignment_details_url(self):
        url = reverse('assignment:details', args=['1'])
        self.assertEquals(resolve(url).func.view_class, AssignmentDetailView) 


    #test for url:  assignment/list<int:pk>
    def test_assignment_submit_url(self):
        url = reverse('assignment:submit')
        self.assertEquals(resolve(url).func.view_class, AssignmentSubmitView) 