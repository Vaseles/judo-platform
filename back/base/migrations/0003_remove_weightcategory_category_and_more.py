# Generated by Django 4.2 on 2023-05-05 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_weightcategory_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weightcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='weightcategory',
            name='slug',
        ),
    ]
