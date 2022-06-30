# Generated by Django 3.1 on 2022-06-30 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210322_0640'),
        ('classroom', '0003_auto_20220629_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroom', to='classroom.classroom'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='users.student'),
        ),
    ]
