from django.db.models import Sum
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Lesson, LessonView, User, ProductUser
from .serializers import ProductSerializer, LessonSerializer, LessonViewSerializer
from typing import List, Dict, Any


# Представление для просмотра уроков пользователя
class UserLessonView(generics.RetrieveAPIView):
    """
    Представление для просмотра уроков, просмотренных пользователем.
    """
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Получает уроки, просмотренные пользователем, и возвращает информацию о них.

        Args:
            request: Запрос.
            args: Аргументы.
            kwargs: Ключевые аргументы, включая 'user_id' - идентификатор пользователя.

        Returns:
            Response: Ответ с информацией о просмотренных уроках пользователя.
        """
        user_id: int = self.kwargs['user_id']

        try:
            user: User = User.objects.get(id=user_id)

            # Получаем все продукты, связанные с пользователем
            products: List[Product] = Product.objects.filter(productuser__user=user)

            # Собираем все уроки, учитывая только уникальные
            lessons: List[Lesson] = Lesson.objects.filter(product__in=products).distinct()

            lesson_data: List[Dict[str, Any]] = []
            for lesson in lessons:
                # Получаем данные о просмотрах урока для конкретного пользователя
                lesson_views: List[LessonView] = LessonView.objects.filter(lesson_product_id__lesson=lesson, user=user)
                lesson_view_serializer = LessonViewSerializer(lesson_views, many=True)

                lesson_info: Dict[str, Any] = {
                    'data': LessonSerializer(lesson).data,
                    'views': lesson_view_serializer.data,
                }

                lesson_data.append(lesson_info)

            response_data: Dict[str, List[Dict[str, Any]]] = {
                'lessons': lesson_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


# Представление для просмотра уроков конкретного продукта пользователя
class UserProductLessonView(generics.RetrieveAPIView):
    """
    Представление для просмотра уроков, просмотренных пользователем на конкретном продукте.
    """
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Получает уроки, просмотренные пользователем на конкретном продукте, и возвращает информацию о них.

        Args:
            request: Запрос.
            args: Аргументы.
            kwargs: Ключевые аргументы, включая 'user_id' - идентификатор пользователя,
                    и 'product_id' - идентификатор продукта.

        Returns:
            Response: Ответ с информацией о просмотренных уроках пользователя на продукте.
        """
        user_id: int = self.kwargs['user_id']
        product_id: int = self.kwargs['product_id']

        try:
            user: User = User.objects.get(id=user_id)

            # Фильтруем продукты по пользователю и конкретному продукту
            products: List[Product] = Product.objects.filter(id=product_id, productuser__user=user)

            if not products.exists():
                return Response({'error': 'Продукт не найден'}, status=status.HTTP_404_NOT_FOUND)

            # Собираем все уроки, учитывая только уникальные
            lessons: List[Lesson] = Lesson.objects.filter(product__in=products).distinct()

            lesson_data: List[Dict[str, Any]] = []

            for lesson in lessons:
                # Получаем данные о просмотрах урока для конкретного пользователя
                lesson_views: List[LessonView] = LessonView.objects.filter(lesson_product_id__lesson=lesson, user=user)
                lesson_view_serializer = LessonViewSerializer(lesson_views, many=True)

                lesson_info: Dict[str, Any] = {
                    'data': LessonSerializer(lesson).data,
                    'views': lesson_view_serializer.data,
                }

                lesson_data.append(lesson_info)

            response_data: Dict[str, List[Dict[str, Any]]] = {
                'lessons': lesson_data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)


# Представление для получения информации о продуктах
class ProductInfoView(APIView):
    """
    Представление для получения информации о продуктах и их использовании.
    """

    def get(self, request) -> Response:
        """
        Получает информацию о продуктах и возвращает статистику использования.

        Args:
            request: Запрос.

        Returns:
            Response: Ответ с информацией о продуктах и их использовании.
        """
        products: List[Product] = Product.objects.all()

        product_info: List[Dict[str, Any]] = []
        total_users: int = User.objects.count()

        for product in products:
            num_users_on_product: int = ProductUser.objects.filter(product=product).count()

            total_views: int = LessonView.objects.filter(lesson_product_id__product=product).count()

            total_time_spent: int = \
            LessonView.objects.filter(lesson_product_id__product=product).aggregate(Sum('view_time_seconds'))[
                'view_time_seconds__sum']

            if total_users > 0:
                purchase_percentage: float = (num_users_on_product / total_users) * 100
            else:
                purchase_percentage: float = 0

            product_info.append({
                'product_id': product.id,
                'num_users_on_product': num_users_on_product,  # Количество учеников занимающихся на продукте
                'total_views': total_views,  # Количество просмотренных уроков от всех учеников
                'total_time_spent': total_time_spent,  # Сколько все ученики потратили времени на просмотр роликов
                'purchase_percentage': purchase_percentage  # Процент приобретения продукта
            })

        return Response(product_info)
