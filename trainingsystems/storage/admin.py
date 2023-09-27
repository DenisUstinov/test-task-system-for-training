from django.contrib import admin
from .models import Owner, Product, ProductUser, Lesson, LessonProduct, LessonView

admin.site.register(Owner)
admin.site.register(Product)
admin.site.register(ProductUser)
admin.site.register(Lesson)
admin.site.register(LessonProduct)
admin.site.register(LessonView)
