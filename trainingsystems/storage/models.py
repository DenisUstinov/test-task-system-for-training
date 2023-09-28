from django.db import models
from django.contrib.auth.models import User


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)


class ProductUser(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'user')


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    link_to_video = models.URLField()
    duration = models.IntegerField()
    product = models.ManyToManyField(Product, through='LessonProduct')


class LessonProduct(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lesson', 'product')


class LessonView(models.Model):
    lesson_product_id = models.ForeignKey(LessonProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_time_seconds = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Получить связанный объект LessonProduct
        lesson_product = self.lesson_product_id

        # Получить объект Lesson, связанный с этим LessonProduct
        lesson = lesson_product.lesson

        if self.view_time_seconds > lesson.duration * 0.8:
            self.is_completed = True
        super(LessonView, self).save(*args, **kwargs)


