# Generated by Django 3.2.8 on 2021-11-17 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chinese_food_recipes', '0005_recipes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipes',
            name='author',
        ),
    ]