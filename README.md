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
git clone <URL_РЕПОЗИТОРИЯ>
cd <ПАПКА_РЕПОЗИТОРИЯ>

```
Настройка переменных окружения:

Создайте файл .env в корневой директории проекта и заполните необходимые переменные окружения. Пример:

```
DEBUG=True
SECRET_KEY=mysecretkey
DATABASE_URL=postgres://user:password@db:5432/db_name
```

Запуск контейнеров

Запустите Docker Compose для сборки и запуска контейнеров:
```
docker-compose up -d --build
```
Применение миграций
После запуска контейнеров, примените миграции:
```
docker-compose exec app bash -c "python manage.py migrate"
```
Создание суперпользователя
Если нужно, создайте суперпользователя:
```
docker-compose exec app bash -c "python manage.py createsuperuser"
```
Статические файлы

Соберите статические файлы (если нужно):
```
docker-compose exec app bash -c "python manage.py collectstatic --noinput"
```
Запуск Celery
```
docker-compose exec app bash -c "celery -A config.celery worker --loglevel=info"
```
и
```
docker-compose exec app bash -c "celery -A config.celery beat --loglevel=info"
```


### Заходим в панель админимстратора, вводим данные нашего пользователя
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
