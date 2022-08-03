# Foodgram - продуктовый помощник.

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Шаблон наполнения env-файла:
``` DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql ```

``` DB_NAME=postgres # имя базы данных ```

``` POSTGRES_USER=postgres # логин для подключения к базе данных ```

``` POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой) ```

``` DB_HOST=db # название сервиса (контейнера) ```

``` DB_PORT=5432 # порт для подключения к БД ```

``` SECRET_KEY='' # секретный ключ Django ```

``` DEBUG=True/False # Включить/отключить режим отладки ```


## Стэк технологий:
  Python 3.7, django 2.2.16, drf 3.2.14, psycopg2-binary 2.8.6, djoser 2.1.0, gunicorn 20.1.0

## Установка:
* Зайдите на ваш удаленный сервер;
* Клонируйте репозиторий себе на удаленный сервер:

  ``` git clone git@github.com:Glaser1/foodgram-project-react.git ```
* Установите docker и docker-compose согласно официальной инструкции (в зависимости от операционной системы сервера):
    https://docs.docker.com/engine/install/    
    https://docs.docker.com/compose/install/
* Перейдите в папку infra репозитория с помощью команды cd infra;
* В файле nginx.conf отредактируйте строку server_name: укажите IP-адрес вашего сервера;
* Создайте файл .env - в нем укажите переменные окружающей среды согласно шаблону выше;

* Запустите приложения в контейнерах: 
  ``` docker-compose up -d --build ```
  
* Выполните миграцию в контейнерах: 

  ``` docker-compose exec web python manage.py makemigrations ```
  
  ``` docker-compose exec web python manage.py migrate ```
* Создайте суперпользователя Django:

  ``` docker-compose exec web python manage.py createsuperuser ```
* Соберите статику:

  ``` docker-compose exec web python manage.py collectstatic --no-input ```
* Загрузите предустановленный список ингредиентов в базу данных:
  ``` docker-compose exec web python manage.py load_data ```
* Проект будет доступен по публичному IP вашего сервера;


