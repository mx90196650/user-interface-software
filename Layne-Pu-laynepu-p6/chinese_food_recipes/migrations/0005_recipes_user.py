# Generated by Django 3.2.8 on 2021-11-14 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chinese_food_recipes', '0004_recipes_collected_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipes',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
