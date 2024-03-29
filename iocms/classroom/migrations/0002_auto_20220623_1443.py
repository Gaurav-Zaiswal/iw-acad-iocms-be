# Generated by Django 3.1 on 2022-06-23 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210322_0640'),
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['creation_date'], 'verbose_name_plural': 'classrooms'},
        ),
        migrations.AlterModelOptions(
            name='classroomstudents',
            options={'verbose_name_plural': 'classroom_students'},
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
                ('rated_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'verbose_name_plural': 'ratings',
            },
        ),
    ]
