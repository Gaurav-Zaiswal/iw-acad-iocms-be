from django.core.mail import send_mail #To send email
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags

from iocms.settings import EMAIL_HOST_USER




def send_email(request, assignemnt_model, student_model, serializer):

    id_of_new_assignemnt = serializer.data["id"]
    new_assignment_data = assignemnt_model.objects.get(id=id_of_new_assignemnt)
    student_email_list = []
    for student in student_model.enrolled_student_id.all():
        student_email_list.append(student.user.email)
    
    # print(student_email_list)
        
    email_subject = f'New assignment posted by {new_assignment_data.teacher}'
    current_site = get_current_site(request)

    html_message = render_to_string('assignment/email_template/email.html',{
        'teacher' : new_assignment_data.teacher,
        'deadline' : new_assignment_data.deadline,
        'domain' : current_site.domain,
        'pk' : id_of_new_assignemnt,
    })
    message = strip_tags(html_message)
    send_mail(subject=email_subject, 
              message=message,
              from_email=EMAIL_HOST_USER,
              # from_email="jr.gaurav2015@gmail.com",
              recipient_list=student_email_list,
              html_message= html_message,
              fail_silently=False
            )
    
    