# Generated by Django 3.2.8 on 2021-11-03 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chinese_food_recipes', '0002_recipes_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='imgSrc',
            field=models.CharField(default='', max_length=200),
        ),
    ]
