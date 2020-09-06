# Generated by Django 3.0.8 on 2020-09-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_classroomfeed_posted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroomfeed',
            name='assignment_description',
        ),
        migrations.RemoveField(
            model_name='classroomfeed',
            name='assignment_title',
        ),
        migrations.AddField(
            model_name='classroomfeed',
            name='feed_description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddConstraint(
            model_name='classroomfeed',
            constraint=models.CheckConstraint(check=models.Q(('assignment_id__isnull', False), ('feed_description__isnull', False), _connector='OR'), name='both_not_null'),
        ),
    ]