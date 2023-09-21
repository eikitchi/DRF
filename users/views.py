from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers.serializers import UsersSerializers, ForAuthUserSerializers, ForCreateUserSerializers


class UsersListView(generics.ListAPIView):
    """
    Получение списка пользователей.

    list:
    Получает список всех пользователей.
    """

    serializer_class = UsersSerializers
    queryset = User.objects.all()


class UsersDetailView(generics.RetrieveAPIView):
    """
    Получение информации о текущем пользователе.

    retrieve:
    Получает информацию о текущем пользователе.
    """

    serializer_class = ForAuthUserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает запрос пользователей в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос пользователей.
        """
        user = self.request.user
        return User.objects.filter(user=user)


class UsersCreateView(generics.CreateAPIView):
    """
    Создание нового пользователя.

    create:
    Создает нового пользователя.
    """

    serializer_class = ForCreateUserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает запрос пользователей в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос пользователей.
        """
        user = self.request.user
        return User.objects.filter(pk=user.id)


class UsersUpdateView(generics.UpdateAPIView):
    """
    Обновление информации о текущем пользователе.

    update:
    Обновляет информацию о текущем пользователе.
    """

    serializer_class = ForCreateUserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает запрос пользователей в зависимости от роли пользователя.

        Returns:
            Queryset: Запрос пользователей.
        """
        user = self.request.user
        return User.objects.filter(pk=user.id)
