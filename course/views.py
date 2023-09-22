import stripe
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks import send_updated_email
from course.paginators import LessonPaginator
from course.serializers.serializers import *
from course.services import create_payment, checkout_session
from config import settings
from users.models import UserRoles

stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    """
    Обзор курсов и их редактирование.

    list:
    Получает список всех курсов.

    create:
    Создает новый курс.

    retrieve:
    Получает информацию о курсе по его ID.

    update:
    Обновляет информацию о курсе по его ID.

    partial_update:
    Обновляет часть информации о курсе по его ID.

    destroy:
    Удаляет курс по его ID.
    """

    serializer_class = CourseSerializers
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def perform_create(self, serializer) -> None:
        """
        Сохраняет новому объекту владельца.

        Args:
            serializer: Сериализатор для создания курса.

        Returns:
            None
        """
        serializer.save(user=self.request.user)  # Сохраняет новому объекту владельца

    def update(self, request, *args, **kwargs):
        send_updated_email.delay(kwargs['pk'])

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        """
        Получает запрос курсов в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос курсов.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)


class LessonListView(generics.ListAPIView):
    """
    Получение списка уроков.

    list:
    Получает список всех уроков.
    """

    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        """
        Получает запрос уроков в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос уроков.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание нового урока.

    create:
    Создает новый урок.
    """

    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def get_queryset(self):
        """
        Получает запрос уроков в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос уроков.
        """
        user = self.request.user
        if user.is_superuser:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonDetailView(generics.RetrieveAPIView):
    """
    Получение информации об уроке.

    retrieve:
    Получает информацию об уроке по его ID.
    """

    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает запрос уроков в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос уроков.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonUpdateView(generics.UpdateAPIView):
    """
    Обновление информации об уроке.

    update:
    Обновляет информацию об уроке по его ID.
    """

    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает запрос уроков в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос уроков.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonDeleteView(generics.DestroyAPIView):
    """
    Удаление урока.

    destroy:
    Удаляет урок по его ID.
    """

    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]  # , IsOwner]

    def get_queryset(self):
        """
        Получает запрос уроков в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос уроков.
        """
        user = self.request.user
        if user.is_superuser:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class PaymentsListView(generics.ListAPIView):
    """
    Получение списка платежей.

    list:
    Получает список всех платежей.
    """

    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_type', 'course', 'lesson']
    filterset_class = FilterSet
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Создание подписки на курс.

    create:
    Создает новую подписку на курс.
    """

    serializer_class = SubscriptionCourseSerialisers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    """
    Обновление информации о подписке на курс.

    update:
    Обновляет информацию о подписке на курс по его ID.
    """

    serializer_class = SubscriptionCourseSerialisers
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateView(generics.CreateAPIView):
    """
    Создание нового платежа.

    create:
    Создает новый платеж.
    """

    serializer_class = PaymentCreateSerializers
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = checkout_session(
            course=serializer.validated_data['payed_course'],
            user=self.request.user
        )
        serializer.save()
        create_payment(course=serializer.validated_data['payed_course'],
                       user=self.request.user)
        return Response(session['id'], status=status.HTTP_201_CREATED)


class GetPaymentView(APIView):
    """
    Получение информации о платеже.

    get:
    Получает информацию о платеже по его ID.
    """

    def get(self, request, payment_id):
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return Response({
            'status': payment_intent.status, })