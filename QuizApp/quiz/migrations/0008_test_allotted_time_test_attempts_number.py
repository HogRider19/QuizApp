# Generated by Django 4.1.3 on 2022-11-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_alter_test_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='allotted_time',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='test',
            name='attempts_number',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
