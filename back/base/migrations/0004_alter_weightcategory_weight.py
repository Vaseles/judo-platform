# Generated by Django 4.2 on 2023-05-05 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_weightcategory_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightcategory',
            name='weight',
            field=models.ManyToManyField(default=[], to='base.weight'),
        ),
    ]
