from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        """Настройка данных для тестов."""
        self.user = User.objects.create(
            email='test@test1.com',
            is_superuser=True,
        )

        # Проверяем, существует ли курс с ID 1
        try:
            self.course = Course.objects.get(id=1)
        except Course.DoesNotExist:
            # Если курс не существует, создаем его
            self.course = Course.objects.create(
                name='Test',
                description='Test'
            )

        self.user.set_password('123')
        self.user.save()

        response = self.client.post('/api/token/', {'email': 'test@test1.com', 'password': '123'})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'lesson_for_test'

    def test_create_lesson(self):
        """Тест создания модели Lesson"""
        response = self.client.post('/api/lesson/create/', {
            'course': self.course.id,  # Здесь используется ID существующего курса
            'name': 'django',
            'description': 'тема',
            'url_video': 'https://www.youtube.com/watch?v=zJRSRSHrRvg'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
