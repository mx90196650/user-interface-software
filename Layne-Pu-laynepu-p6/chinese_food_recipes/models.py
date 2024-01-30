from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


# Create your models here.

class Recipes(models.Model):
    imgSrc = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    shareNum = models.IntegerField(default=0)
    commentNum = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    num_of_ser = models.IntegerField(default=0)
    prep_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    ingredient = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    tags = ArrayField(models.CharField(max_length=10), default=[])
    collected_by = ArrayField(models.CharField(max_length=50), default=[])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('chinese_food_recipes:recipes_detail_page', args=[self.id])


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
