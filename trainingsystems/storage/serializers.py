from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Owner, Product, ProductUser, Lesson, LessonView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id'


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = 'user'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUser
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ('view_time_seconds', 'is_completed', 'updated_at')
