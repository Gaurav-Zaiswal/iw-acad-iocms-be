from django.db import models
from django.db.models import constraints
from django.utils.timezone import now

from users.models import Teacher, User
from assignment.models import Assignment
from classroom.models import Classroom


class ClassroomFeed(models.Model):
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    assignment_id = models.OneToOneField(Assignment, on_delete=models.CASCADE, null=True)
    posted_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feed_description = models.TextField(max_length=500, null = True)
    posted_on = models.DateTimeField(default=now)

    def __str__(self):
        return f"Feed of {self.classroom_id.class_name} posted by {self.teacher_id.username}"


    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(models.Q(assignment_id__isnull = False) | models.Q(feed_description__isnull = False)),
                name = "both_not_null"
            )
        ]