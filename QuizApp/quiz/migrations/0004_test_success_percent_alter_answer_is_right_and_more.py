# Generated by Django 4.1.3 on 2022-11-08 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_group'),
        ('quiz', '0003_alter_answer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='success_percent',
            field=models.FloatField(default=50.0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_right',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='compiled_questions', to='profiles.profile'),
        ),
    ]
