from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class ProductUser(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    link_to_video = models.URLField()
    duration = models.DurationField()
    products = models.ManyToManyField(Product, through='LessonProduct')


class LessonProduct(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class LessonView(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_time_seconds = models.DurationField(default=0)
    is_completed = models.BooleanField(default=False)
