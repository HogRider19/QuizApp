# Generated by Django 4.1.3 on 2022-11-08 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_test_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='cources',
            field=models.ManyToManyField(related_name='tests', to='quiz.cource'),
        ),
    ]