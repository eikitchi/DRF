## DRF COURSE
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

### Технологии:
- python 3.11
- django 4.2.2
- djangorestframework 3.14.0
- PostgreSQL
- Docker

### Инструкция для развертывания проекта с использованием Docker:

Клонирование проекта:
```
git clone https://github.com/
```
Запуск:

Для запуска проекта необходимо создать .env в директории ..
скопировать в него содержимое файла  .env.example 

Запустить команду, указанную ниже из директории ...
```
docker-compose up -d --build
```

Пример использования:

1. Создать суперпользователя для использования Admin-панели.
Для этого необходимо:
```
docker ps
```
После выполнения команды в консоль выведется список заупщенных контейнеров.
Необходимо скопировать id контейнера backend.
Далее вводим команду:
```
docker exec -it <id контейнера> bash
```
Попадаем в наш контейнер и создаем суперпользователя
```
python manage.py createsuperuser
```
Вводим данные и выходим из контейнера


2. Заходим в панель админимстратора, вводим данные нашего пользователя
```
http://localhost/admin/
```
3. Создаем резюме в разделе резюме
4. Отправляем GET запрос на эндпоинт - чтобы получить данные по ...:
```
http://localhost/...
```
4. Для доступа к эндпоинту изменения резюме необходимо авторизовать пользователя.
Для этого отправляем POST-запрос на эндпоинт:
```
http://localhost/token/
```
Тело запроса должно быть в формате Json и выглядеть примерно так:
```
{
    "username": "alex",
    "password": "123qwe"
}
```
Далее копируем токен и вставляем его в заголовок Authorization в формате Bearer <наш токен>

С уже имеющимся токеном отправляем PATCH запрос для изменения резюме на эндпоинт:
```
http://localhost/resume/<id-резюме>
```
Body в запросе должно быть в формате Json с указанием полей и значений для изменения
```
{
    "title": "new_title"
}
```
Посмотреть все реализованные эндпоинты можно по адресу:
```
http://localhost/swagger
```
