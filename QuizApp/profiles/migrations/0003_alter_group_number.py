# Generated by Django 4.1.3 on 2022-11-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_group_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='number',
            field=models.CharField(default='0', max_length=1, unique=True),
        ),
    ]
