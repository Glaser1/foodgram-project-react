# Foodgram - продуктовый помощник.

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Шаблон наполнения env-файла:
``` DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql ```

``` DB_NAME=postgres # имя базы данных ```

``` POSTGRES_USER=postgres # логин для подключения к базе данных ```

``` POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой) ```

``` DB_HOST=db # название сервиса (контейнера) ```

``` DB_PORT=5432 # порт для подключения к БД ```
``` SECRET_KEY='' # секретный ключ Django ```
``` DEBUG=True/False # Включить/отключить режим отладки ```

## Установка:
* Зайдите на ваш удаленный сервер;
* Клонируйте репозиторий себе на удаленный сервер:
  ``` git clone git@github.com:Glaser1/foodgram-project-react.git ```
* Установите docker и docker-compose по официальной инструкции (в зависимости от операционной системы сервера):
    https://docs.docker.com/engine/install/    
    https://docs.docker.com/compose/install/
* Перейдите в папку infra репозитория с помощью команды cd infra;

* Запустите приложения в контейнерах с помощью команды docker-compose up
* Выполните миграцию в контейнерах: 

  ``` docker-compose exec-web python manage.py makemigrations ```
  
  ``` docker-compose exec-web python manage.py migrate ```


